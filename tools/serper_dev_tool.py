from langchain_community.utilities import GoogleSerperAPIWrapper
from utils import load_api 
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

class SerperDevTool:
    def __init__(self):
        self.api = GoogleSerperAPIWrapper()
    
    def scrape_trends(self):
        queries = ["latest fashion trends on TikTok", "popular beauty trends on Instagram", "trending apparel on Facebook"]
        trends = {}
        for query in queries:
            results = self.api.run(query)
            trends[query] = results
        return trends