import os, sys
import json
# import numpy as np

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

# from crewai import Agent, Task, Crew
# from langchain.llms import OpenAI
from langchain.tools import tool
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.configs import load_config
from utils.helpers import load_json_file

# Ensure you have set your OpenAI API key in your environment variables
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize the sentence transformer model
model_str = load_config('tools')['product_intelligence_analyzer']['llm']['sentence_transformer']
model = SentenceTransformer(model_str)

# Helper functions
def load_trends(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_products(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_embedding(text):
    return model.encode(text)

def compute_similarity(embed1, embed2):
    return cosine_similarity([embed1], [embed2])[0][0]


class ProductAnalyzerTool:
    @tool("Product Intelligence Analyzer")
    def product_intelligence_analyzer(trends: str) -> str:
        """Analyze product intelligence data to find relevant products for given trends using text embeddings."""
        trends_data = json.loads(trends)
        
        product_data = load_json_file('data/realistic_products.json')
        
        all_relevant_products = []
        
        for trend in trends_data:
            # Create trend embedding
            trend_text = f"{trend['trend']} {trend['category']} {' '.join(trend['subcategories'])} {' '.join(trend['products'])}"
            trend_embedding = get_embedding(trend_text)
            
            relevant_products = []
            for product in product_data:
                relevance_score = 0
                
                # Create product embedding
                product_text = f"{product['productName']} {product['category']} {product['subCategory']} {product['productDescription']}"
                product_embedding = get_embedding(product_text)
                
                # Compute similarity
                similarity = compute_similarity(trend_embedding, product_embedding)
                
                # Base relevance score on similarity
                relevance_score += similarity * 5  # Scale similarity to 0-5 range
                
                # Additional exact matching bonuses
                if product['category'].lower() == trend['category'].lower():
                    relevance_score += 1
                if product['subCategory'].lower() in [sub.lower() for sub in trend['subcategories']]:
                    relevance_score += 1
                if product['brand'] in trend['brands']:
                    relevance_score += 1
                
                # If the product is relevant enough, add it to the list
                if relevance_score >= 3:
                    relevant_products.append({
                        "product": product,
                        "relevance_score": relevance_score,
                        "similarity": similarity,
                        "trend": trend['trend']
                    })
            
            # Sort products by relevance score for this trend
            relevant_products.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Add top 5 products for this trend to the overall list
            all_relevant_products.extend(relevant_products[:5])
        
        # Sort all products by relevance score
        all_relevant_products.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return json.dumps(all_relevant_products)
