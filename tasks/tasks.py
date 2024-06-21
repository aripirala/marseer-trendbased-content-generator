from crewai import Task
from textwrap import dedent

class TrendbasedArticleGeneratorTasks:
    def capture_social_media_trends(self, 
                                    agent,
                                    output_dir,
                                    social_media_platforms=['instagram', 'facebook'], 
                                    product_categories=['apparel']):
            description = dedent(f"""\
                                Actively search the internet and various social media platforms - {social_media_platforms} to identify 
                                the latest trends between 06/01/2024 to 06/15/2024, in the following product categories: {product_categories}, 
                                and any other relevant categories you want to include.
                                
                                capture at least 5 trends
                                
                                For each identified trend, gather the following information:
                                - Platform (e.g., Instagram, Twitter, TikTok, etc.)
                                - Trend description -  give example products that trended. explain why they trended? (up to 50 words)
                                - Product category (apparel, beauty, etc.)
                                - Sub-categories or specific product types
                                - products - linen shirts, blue summer dress
                                - product brands - nike, patagonia etc.
                                - Date when the trend was observed
                                - Any other relevant metadata or context

                                Organize the collected information into a JSON format, with each trend represented as an 
                                object within an array. The JSON structure should be as follows:

                                [
                                    {{
                                        "platform": "...",
                                        "trend": "...",
                                        "category": "...", 
                                        "subcategories": [...],
                                        "date": "...",
                                        "metadata": {{...}}
                                    }},
                                    {{...}}
                                ]
                                The 'metadata' field can include additional details like influencers promoting the trend, hashtags, or any other relevant information.
                            """)
            expected_output="A JSON object containing the latest trends organized by platform, product category, and relevant metadata."
            # print(description)
            task = Task(description=description, 
                        agent=agent, 
                        expected_output=expected_output
                        )
            return task
    
if __name__=='__main__':
      task = TrendbasedArticleGeneratorTasks().capture_social_media_trends(agent="tommy")

                                    