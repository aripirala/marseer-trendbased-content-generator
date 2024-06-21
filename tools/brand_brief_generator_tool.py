from llms.gpt4 import GPT4

class BrandBriefGeneratorTool:
    def __init__(self):
        self.llm = GPT4()

    def generate_brand_briefs(self, trend_product_mapping):
        briefs = {}
        for platform, trends in trend_product_mapping.items():
            sorted_trends = sorted(trends, key=lambda x: x['relevancy_score'], reverse=True)[:10]
            briefs[platform] = [{"trend": trend["trend"], "brief": self.llm.create_brief(trend)} for trend in sorted_trends]
        return briefs