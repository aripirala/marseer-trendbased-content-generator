import json
import os
import sys

# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from llms.LLM import LLM 


class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing researches and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
          allow_delegation=False,
          llm=LLM(execution_type='groq', model='llama3_70b').get_llm())
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
          expected_output="summary of the website in the string format"
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)