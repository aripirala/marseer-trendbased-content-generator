from crewai import Task
from textwrap import dedent
import datetime

class TrendbasedArticleGeneratorTasks:
    # def capture_social_media_trends(self, 
    #                                 agent,
    #                                 output_dir,
    #                                 social_media_platforms=['instagram', 'facebook'], 
    #                                 product_categories=['apparel']):
    #         description = dedent(f"""\
    #                             Actively search the internet and various social media platforms - {social_media_platforms} to identify 
    #                             the latest trends between 06/01/2024 to 06/15/2024, in the following product categories: {product_categories}, 
    #                             and any other relevant categories you want to include.
                                
    #                             capture at least 5 trends
                                
    #                             For each identified trend, gather the following information:
    #                             - Platform (e.g., Instagram, Twitter, TikTok, etc.)
    #                             - Trend description -  give example products that trended. explain why they trended? (up to 50 words)
    #                             - Product category (apparel, beauty, etc.)
    #                             - Sub-categories or specific product types
    #                             - products - linen shirts, blue summer dress
    #                             - product brands - nike, patagonia etc.
    #                             - Date when the trend was observed
    #                             - Any other relevant metadata or context

    #                             Organize the collected information into a JSON format, with each trend represented as an 
    #                             object within an array. The JSON structure should be as follows:

    #                             [
    #                                 {{
    #                                     "platform": "...",
    #                                     "trend": "...",
    #                                     "category": "...", 
    #                                     "subcategories": [...],
    #                                     "date": "...",
    #                                     "metadata": {{...}}
    #                                 }},
    #                                 {{...}}
    #                             ]
    #                             The 'metadata' field can include additional details like influencers promoting the trend, hashtags, or any other relevant information.
    #                         """)
    #         expected_output="A JSON object containing the latest trends organized by platform, product category, and relevant metadata."
    #         # print(description)
    #         task = Task(description=description, 
    #                     agent=agent, 
    #                     expected_output=expected_output
    #                     )
    #         return task
    
    def task_trend_research(self, agent, run_id=None): 
        expected_output="A JSON object containing the latest trends organized by platform, product category, and relevant metadata."
        

        # Format timestamp as a string
        if run_id:
            task_output_file_name = f"{run_id}/{run_id}-trends.json"
        task = Task(
                description="Search for the latest trends in apparel from the last 2 weeks",
                agent=agent, expected_output=expected_output, output_file=f'data/{task_output_file_name}')
        return task

    
    def trend_based_product_analysis(self, agent, run_id=None):

        if run_id:
            task_output_file_name = f"{run_id}/{run_id}-Product-trends.json"

        expected_output = 'JSON object containing -  Trend, Platform, Products, Category and any other relevant information'

        task = Task(
                description='Analyze our product data and identify items that align with the current trends. Provide a list of products we can promote.',
                agent=agent, expected_output=expected_output, output_file=f'data/{task_output_file_name}')

        return task
    
    def write_engaging_content(self, agent, run_id=None):
        expected_output = 'JSON object containing article title, content, trend, tags, category'
        if run_id:
            task_output_file_name = f"{run_id}/{run_id}-content.json"
        task = Task(
                    description='Write an engaging article for a landing page that compares the selected products and brands, highlighting how they relate to current trends.',
                    agent=agent,
                    expected_output=expected_output,
                    output_file=f'data/{task_output_file_name}'
                )
        return task
    
    def write_brand_brief(self, agent):
        expected_output = 'Markdown object'

        task = Task(
            description='Create a brand brief that will guide the creation of ad copy to promote the selected products, current trends, and the landing page.',
            agent=agent,
            expected_output=expected_output
        )
        return task
    
if __name__=='__main__':
      task = TrendbasedArticleGeneratorTasks().capture_social_media_trends(agent="tommy")

                                    