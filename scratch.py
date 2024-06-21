from textwrap import dedent

platforms = "Instagram, Twitter, TikTok, etc."

string = dedent(f"""\
    Actively search the internet and various social media platforms to identify the latest trends in the following product categories: apparel, beauty, and any other relevant categories you want to include.

    For each identified trend, gather the following information:
    - Platform (e.g., {platforms})
    - Trend name or description
    - Product category (apparel, beauty, etc.)
    - Sub-categories or specific product types
    - Date when the trend was observed
    - Any other relevant metadata or context

    Organize the collected information into a JSON format, with each trend represented as an object within an array. The JSON structure should be as follows:

    [
        {{
            "platform": "...",
            "trend": "...",
            "category": "...", 
            "subcategories": [...],
            "date": "...",
            "metadata": {{}}
        }},
        {{}}
    ]
    The 'metadata' field can include additional details like influencers promoting the trend, hashtags, or any other relevant information.
""")

print(string)