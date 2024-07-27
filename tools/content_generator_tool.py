import os, sys
import json
import random
from datetime import datetime
# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

# from crewai import Agent, Task, Crew
# from langchain.llms import OpenAI
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.configs import load_config
from llms.LLM import LLM

# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

class ContentGeneratorTool:

    @tool("Content Generator")
    def content_generator(trends: str, all_relevant_products: str) -> str:
        """Generate compelling article content based on trends and relevant products, outputting in a specific JSON format."""
        trends_data = json.loads(trends)
        all_products_data = json.loads(all_relevant_products)
        tools_configs = load_config('tools')

        template_selector_llm = LLM(execution_type_model=tools_configs['template_generator']['llm']['template_selector']).get_llm()      #OpenAI(temperature=0.7)
        content_generator_llm = LLM(execution_type_model=tools_configs['content_generator']['llm']['template_selector']).get_llm()
        title_generator_llm = LLM(execution_type_model=tools_configs['title_generator']['llm']['template_selector']).get_llm()
        tags_generator_llm = LLM(execution_type_model=tools_configs['tags_generator']['llm']['template_selector']).get_llm()

        # Template selection prompt
        template_selection_prompt = PromptTemplate(
            input_variables=["trend", "category"],
            template="Given a fashion trend '{trend}' in the category '{category}', suggest an engaging article template that will maximize visitor engagement. The template should include placeholders for key information and have a compelling structure."
        )
        
        template_selector = LLMChain(llm=template_selector_llm, prompt=template_selection_prompt)
        
        # Content generation prompt
        content_generation_prompt = PromptTemplate(
            input_variables=["template", "trend", "platform", "date", "category", "brands", "products", "influencers", "hashtags", "top_products"],
            template="""
            Using the following template:

            {template}

            Generate a compelling article about the '{trend}' trend. Include the following information:
            Platform: {platform}
            Date: {date}
            Category: {category}
            Featured Brands: {brands}
            Key Products: {products}
            Influencers: {influencers}
            Hashtags: {hashtags}

            Top Products:
            {top_products}

            Ensure the content is engaging, informative, and likely to maximize visitor engagement. Use a conversational tone, include calls-to-action, and highlight the unique aspects of the trend and products. Integrate the top products seamlessly into the article, emphasizing their relevance to the trend.
            """
        )
        
        content_generator = LLMChain(llm=content_generator_llm, prompt=content_generation_prompt)
        
        # Title generation prompt
        title_generation_prompt = PromptTemplate(
            input_variables=["trend", "category", "content"],
            template="Based on the following trend '{trend}' in the category '{category}' and the article content:\n\n{content}\n\nGenerate an engaging and SEO-friendly title for the article."
        )
        
        title_generator = LLMChain(llm=title_generator_llm, prompt=title_generation_prompt)
        
        # Tags generation prompt
        tags_generation_prompt = PromptTemplate(
            input_variables=["trend", "category", "content"],
            template="Based on the following trend '{trend}' in the category '{category}' and the article content:\n\n{content}\n\nGenerate 3-5 relevant tags for the article. Return the tags as a comma-separated list."
        )
        
        tags_generator = LLMChain(llm=tags_generator_llm, prompt=tags_generation_prompt)
        
        articles = []
        
        for trend in trends_data:
            # Filter relevant products for this trend
            trend_products = [p for p in all_products_data if p['trend'] == trend['trend']]
            trend_products.sort(key=lambda x: x['relevance_score'], reverse=True)
            top_products = trend_products[:3]  # Get top 3 products for this trend
            
            # Prepare top products information
            top_products_info = "\n".join([
                f"- {p['product']['brand']} {p['product']['productName']}: ${p['product']['productPrice']}\n"
                f"  {p['product']['productDescription']}\n"
                f"  Relevance Score: {p['relevance_score']:.2f}/8"
                for p in top_products
            ])
            
            # Select template
            template = template_selector.run(trend=trend['trend'], category=trend['category'])
            
            # Generate content
            content = content_generator.run(
                template=template,
                trend=trend['trend'],
                platform=trend['platform'],
                date=trend['date'],
                category=trend['category'],
                brands=", ".join(trend['brands']),
                products=", ".join(trend['products']),
                influencers=", ".join(trend['metadata']['influencers']),
                hashtags=", ".join(trend['metadata']['hashtags']),
                top_products=top_products_info
            )
            
            # Generate title
            title = title_generator.run(trend=trend['trend'], category=trend['category'], content=content)
            
            # Generate tags
            tags = tags_generator.run(trend=trend['trend'], category=trend['category'], content=content)
            
            # Create article JSON
            article = {
                "title": title.strip(),
                "author": "",
                "content": content.strip(),
                "imageLinks": [f"https://example.com/{trend['trend'].replace(' ', '_').lower()}_image.jpg"],
                "category": trend['category'],
                "tags": [tag.strip() for tag in tags.split(',')],
                "featured": random.choice([True, False]),
                "date": datetime.now().strftime("%b %d, %Y"),
                "views": random.randint(100, 1000),
                "likes": random.randint(10, 100)
            }
            
            articles.append(article)
        
        return json.dumps(articles, indent=2)
