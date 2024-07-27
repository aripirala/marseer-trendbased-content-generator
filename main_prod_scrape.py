import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json
from dotenv import load_dotenv

load_dotenv()

from llms.LLM import LLM

# Set your environment variables
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
BROWSERLESS_API_KEY = os.environ.get('BROWSERLESS_API_KEY')
landing_page = 'https://bonobos.com/shop/clothing/shirts'

def fetch_page_content(url):
    browserless_api_url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"
    payload = json.dumps({"url": url})
    headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
    response = requests.post(browserless_api_url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None

def chunk_html(html_content, chunk_size=500):
    soup = BeautifulSoup(html_content, 'html.parser')
    chunks = []
    current_chunk = ""
    for tag in soup.recursiveChildGenerator():
        if isinstance(tag, str):
            current_chunk += tag
            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk)
                current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def analyze_page_structure(html_chunk):
    soup = BeautifulSoup(html_chunk, 'html.parser')
    
    possible_product_links = [
        soup.select('a.product-link'),
        soup.select('div.product-item a'),
        soup.select('li.product a'),
        soup.select('a[href*="product"]'),
    ]
    
    possible_pagination = [
        soup.select('a.pagination-link'),
        soup.select('div.pagination a'),
        soup.select('ul.pagination li a'),
        soup.select('a[href*="page="]'),
    ]
    
    return {
        'possible_product_links': [str(link) for sublist in possible_product_links for link in sublist],
        'possible_pagination': [str(link) for sublist in possible_pagination for link in sublist],
    }

# Tools
fetch_page_tool = Tool(
    name="FetchPage",
    description="Fetches the content of a web page using Browserless.io",
    func=fetch_page_content
)

analyze_structure_tool = Tool(
    name="AnalyzeStructure",
    description="Analyzes the HTML structure of a page to identify potential product links and pagination",
    func=analyze_page_structure
)

llm = LLM(execution_type_model='groq-llama3_70b').get_llm()

# Agents
researcher = Agent(
    role='Website Researcher',
    goal='Analyze website structure and find product pages',
    backstory='You are an expert at understanding website structures and identifying patterns for product pages and navigation',
    tools=[fetch_page_tool, analyze_structure_tool],
    llm=llm,
    verbose=True
)

scraper = Agent(
    role='Web Scraper',
    goal='Extract detailed product information from web pages',
    backstory='You are an expert at parsing HTML and extracting structured data from various website layouts',
    tools=[fetch_page_tool],
    llm=llm,
    verbose=True
)

analyzer = Agent(
    role='Data Analyzer',
    goal='Analyze and structure the scraped product information',
    backstory='You are an expert at organizing, cleaning, and structuring data from various sources',
    llm=llm,
    verbose=True
)


# Tasks
research_task = Task(
    description=f"""
    1. Start from the main product category page: {landing_page}
    2. Use the FetchPage tool to get the page content.
    3. Chunk the HTML content into smaller pieces.
    4. For each chunk, use the AnalyzeStructure tool to identify potential product links and pagination.
    5. Combine the results from all chunks to determine the most likely selectors for product links and pagination.
    6. Use these selectors to identify product URLs across multiple pages.
    7. Return a list of up to 10 product page URLs and the identified selectors for future use.
    
    Be adaptive and try different approaches if the initial analysis doesn't yield good results.
    If you encounter any errors related to request size, try working with smaller chunks of data.
    """,
    agent=researcher,
    expected_output = 'List of product page URLs and the identified selectors for future use.'
)

scrape_task = Task(
    description="""
    Using the list of product URLs and selectors provided by the researcher:
    1. For each product page URL, use the FetchPage tool to get the page content.
    2. Chunk the HTML content if necessary to avoid request size limitations.
    3. Analyze the HTML structure to locate key product information:
       - Product name
       - Price
       - Description (limit to 100 words)
       - Features (list up to 5 key features)
       - Customer reviews (if available, limit to 3 recent reviews)
    4. Extract this information for each product.
    5. If the provided selectors don't work, adapt and find alternative ways to extract the information.
    6. Return the scraped data for each product, ensuring the total response size remains manageable.
    """,
    agent=scraper,
    expected_output = 'Json of product information'
)

analyze_task = Task(
    description="""
    1. Review the scraped product information from the Web Scraper.
    2. Organize and structure the data into a consistent format across all products.
    3. Identify any missing or inconsistent information.
    4. Clean the data, removing any HTML tags or unnecessary whitespace.
    5. Standardize formats (e.g., prices, dates) across all products.
    6. Prepare a concise summary report including:
       - Total number of products scraped
       - Brief overview of data quality and completeness
       - Any notable patterns or insights (limit to 3-5 key points)
    7. Format the final data as a well-structured JSON object, ensuring the total size remains under 4000 tokens.
    """,
    agent=analyzer,
    expected_output = 'Well Structured Json object'
)

# Create Crew
product_scraping_crew = Crew(
    agents=[researcher, scraper, analyzer],
    tasks=[research_task, scrape_task, analyze_task],
    verbose=2
)

# Run the crew
result = product_scraping_crew.kickoff()

# Save the result
with open('scraped_products.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Scraping completed. Results saved to scraped_products.json")