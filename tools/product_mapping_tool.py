class ProductMappingTool:
    def __init__(self, product_intelligence):
        self.product_intelligence = product_intelligence

    def map_trends_to_products(self, trends):
        mapping = {}
        for platform, trend_list in trends.items():
            mapping[platform] = [{"trend": trend, "products": self.product_intelligence.get(trend, []), "relevancy_score": 0.9} for trend in trend_list]
        return mapping