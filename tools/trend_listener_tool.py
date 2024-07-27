import json
# import re
# from datetime import datetime, timedelta
from typing import List, Dict
from crewai import Agent, Task, Crew
# from langchain.llms import OpenAI
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Assuming these are imported from your existing codebase
from tools.search_tools import SearchTools
from tools.browser_tool import BrowserTools
from llms.LLM import LLM
from utils.configs import load_config

def safe_json_loads(json_string: str, default_value: any = None) -> any:
    """Safely load JSON string, returning a default value if it fails."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Problematic JSON string: {json_string}")
        return default_value

# class TrendListenerTools:
#     @tool("Web Scraper")
#     def web_scraper(query: str) -> str:
#         """
#         Scrape the web for recent trends in fashion, combining data from internet searches,
#         social media, and website content.
#         """
#         # llm = OpenAI(temperature=0.7)
#         # query = scrape_query['query']
#         tool_configs = load_config('tools')
#         llm = LLM(execution_type_model=tool_configs['website_scraper']['llm']['trend_analyzer']).get_llm()

#         search_tools = SearchTools()
#         browser_tool = BrowserTools()
        
#         try:
#             # Step 1: Perform initial internet search
#             search_results = search_tools.search_internet(query) #f"latest fashion trends in {query}")
#             print(f"Search results: {search_results}")

#             # Step 2: Extract potential trends and perform deeper analysis
#             trend_analyzer_prompt = PromptTemplate(
#                 input_variables=["search_results"],
#                 template="""
#                 Analyze the following search results and identify potential fashion trends:
#                 {search_results}
                
#                 For each potential trend, provide:
#                 1. Trend name
#                 2. Category (e.g., Apparel, Shoes, Accessories)
#                 3. Related keywords or phrases
                
#                 Output the results in a JSON format like this:
#                 [
#                     {{
#                         "trend_name": "Example Trend",
#                         "category": "Example Category",
#                         "related_keywords": ["keyword1", "keyword2"]
#                     }}
#                 ]
#                 """
#             )
            
#             trend_analyzer = LLMChain(llm=llm, prompt=trend_analyzer_prompt)
#             potential_trends_json = json.loads(trend_analyzer.run(search_results=search_results))
#             print(f"Potential trends JSON: {potential_trends_json}")
            
#             potential_trends = safe_json_loads(potential_trends_json, [])
#             if not potential_trends:
#                 return json.dumps({"error": "No potential trends identified"})
            
#             trends = []
#             for pt in potential_trends:
#                 # Step 3: Search social media for each potential trend
#                 instagram_results = search_tools.search_instagram(f"{pt['trend_name']} fashion")
#                 facebook_results = search_tools.search_facebook(f"{pt['trend_name']} fashion")
                
#                 # Step 4: Scrape and summarize top websites for each trend
#                 top_urls = search_tools.search_internet(f"{pt['trend_name']} fashion trend", num_results=3)
#                 website_summaries = [browser_tool.scrape_website_and_summarize(url) for url in top_urls]
                
#                 # Step 5: Analyze and structure the trend information
#                 trend_structurer_prompt = PromptTemplate(
#                     input_variables=["trend_name", "category", "keywords", "instagram_results", "facebook_results", "website_summaries"],
#                     template="""
#                     Based on the following information about the "{trend_name}" trend in the {category} category:
                    
#                     Keywords: {keywords}
#                     Instagram results: {instagram_results}
#                     Facebook results: {facebook_results}
#                     Website summaries: {website_summaries}
                    
#                     Generate a structured trend report in the following JSON format:
#                     {{
#                         "platform": "Determine the most relevant platform",
#                         "trend": "{trend_name}",
#                         "category": "{category}",
#                         "subcategories": ["List", "of", "subcategories"],
#                         "products": ["List", "of", "related", "products"],
#                         "brands": ["List", "of", "mentioned", "brands"],
#                         "date": "Current date range in format MM/DD/YYYY - MM/DD/YYYY",
#                         "metadata": {{
#                             "influencers": ["List", "of", "influencers"],
#                             "hashtags": ["List", "of", "hashtags"]
#                         }}
#                     }}
                    
#                     Ensure all fields are filled based on the provided information.
#                     """
#                 )
#                 trend_structurer = LLMChain(llm=llm, prompt=trend_structurer_prompt)
#                 structured_trend_json = json.loads(trend_structurer.run(
#                     trend_name=pt['trend_name'],
#                     category=pt['category'],
#                     keywords=", ".join(pt['related_keywords']),
#                     instagram_results=instagram_results,
#                     facebook_results=facebook_results,
#                     website_summaries=json.dumps(website_summaries)
#                 ))
                
#                 print(f"Structured trend JSON: {structured_trend_json}")
                
#                 structured_trend = safe_json_loads(structured_trend_json)
#                 if structured_trend:
#                     trends.append(structured_trend)
                
#                 trends.append(structured_trend)
            
#             return json.dumps(trends, indent=2)
        
#         except Exception as e:
#             print(f"Error in web_scraper: {str(e)}")
#             return json.dumps({"error": str(e)})

class TrendListenerTools:
    @tool("Trend Analyzer")
    def trend_analyzer(search_results: str) -> str:
        """
        Analyze search results and identify potential fashion trends.
        """
        # This tool will be used by the TrendAnalyzerAgent
        pass

    @tool("Web Scraper")
    def web_scraper(query: str) -> str:
        """
        Scrape the web for recent trends in fashion, combining data from internet searches,
        social media, and website content.
        """
        # llm = OpenAI(temperature=0.7)
        tool_configs = load_config('tools')
        llm = LLM(execution_type_model=tool_configs['website_scraper']['llm']['trend_analyzer']).get_llm()
        
        try:
            # Step 1: Perform initial internet search
            search_results = SearchTools.search_internet(query) #f"latest fashion trends in {query}")
            print(f"Search results: {search_results}")
            
            # Step 2: Use TrendAnalyzerAgent to extract potential trends
            trend_analyzer_agent = Agent(
                role='Trend Analyzer',
                goal='Analyze search results and identify potential fashion trends',
                backstory='Expert in identifying emerging fashion trends from various data sources',
                tools=[],
                llm=llm,
                verbose=True
            )
            
            trend_analysis_task = Task(
                description=f"""Analyze the following search results and identify potential fashion trends:
                                    {search_results}

                                    For each potential trend, provide:
                                    1. Trend name
                                    2. Category (e.g., Apparel, Shoes, Accessories)
                                    3. Related keywords or phrases

                                    Output the results in a JSON format like this:
                                    [{{
                                        "trend_name": "Example Trend", 
                                        "category": "Example Category",
                                        "sub-categories": ["sub-category-1", "sub-category-2", ... ]
                                        "relevant_products": ["product1", "product2", ...]  
                                        "related_keywords": ["keyword1", "keyword2"]
                                      }}
                                    ]""",
                agent=trend_analyzer_agent,
                expected_output="Json of trends in the right format"                                
            )
            
            potential_trends_json = Crew(
                agents=[trend_analyzer_agent],
                tasks=[trend_analysis_task]
            ).kickoff()
            
            print(f"Potential trends JSON: {potential_trends_json}")
            
            potential_trends = safe_json_loads(potential_trends_json, [])
            if not potential_trends:
                return json.dumps({"error": "No potential trends identified"})
            
            trends = []
            for pt in potential_trends:
                # Step 3: Search social media for each potential trend
                print("searching in social media for trends")
                instagram_results = SearchTools.search_instagram(f"{pt['trend_name']} fashion in the last 2 weeks")
                facebook_results = SearchTools.search_facebook(f"{pt['trend_name']} fashion in the last 2 weeks")
                
                # Step 4: Scrape and summarize top websites for each trend
                                
                top_k = 5
                top_urls = SearchTools.search_internet(f"{pt['trend_name']} fashion trend in the last 2 weeks")
                top_urls = top_urls[:top_k]

                print(f"Scraping website for trends - url count  - {len(top_urls)}. \nFew urls {top_urls[:2]}")
                website_summaries = [BrowserTools.scrape_and_summarize_website(url) for url in top_urls]
                
                # Step 5: Analyze and structure the trend information
                trend_structurer_agent = Agent(
                    role='Trend Structurer',
                    goal='Create structured trend reports based on collected data',
                    backstory='Expert in organizing and presenting fashion trend information',
                    tools=[],  # No specific tools needed for this agent
                    llm=llm,
                    verbose=True
                )
                
                trend_structuring_task = Task(
                    description=f"""Based on the following information about the '{pt["trend_name"]}' trend in the {pt["category"]} category:

                                    Keywords: {', '.join(pt['related_keywords'])}
                                    Instagram results: {instagram_results}
                                    Facebook results: {facebook_results}
                                    Website summaries: {json.dumps(website_summaries)}

                                    Generate a structured trend report in the following JSON format:
                                    {{
                                        "platform": "Determine the most relevant platform",
                                        "trend": "{pt["trend_name"]}",
                                        "category": "{pt["category"]}",
                                        "subcategories": ["List", "of", "subcategories"],
                                        "products": ["List", "of", "related", "products"],
                                        "brands": ["List", "of", "mentioned", "brands"],
                                        "date": "Current date range in format MM/DD/YYYY - MM/DD/YYYY",
                                        "metadata": {{
                                            "influencers": ["List", "of", "influencers"],
                                            "hashtags": ["List", "of", "hashtags"]
                                        }}
                                    }}

                                    Ensure all fields are filled based on the provided information.""",
                    agent=trend_structurer_agent,
                    expected_output="Json of Trend and its relevant metadata"
                )
                
                structured_trend_json = Crew(
                    agents=[trend_structurer_agent],
                    tasks=[trend_structuring_task]
                ).kickoff()
                
                print(f"Structured trend JSON: {structured_trend_json}")
                
                # structured_trend = safe_json_loads(structured_trend_json)
                if structured_trend_json:
                    trends.append(structured_trend_json)
            
            if not trends:
                return json.dumps({"error": "Failed to structure any trends"})
            
            return json.dumps(trends, indent=2)
        
        except Exception as e:
            print(f"Error in web_scraper: {str(e)}")
            return json.dumps({"error": str(e)})
