import json
import random

# Sample data to use for generating products
apparel_categories = ["Tops", "Bottoms", "Outerwear", "Dresses", "Activewear"]
beauty_categories = ["Skincare", "Haircare", "Makeup"]
brands_mid_range = ["Reformation", "NAADAM", "Spanx", "Everlane", "Agolde", "Quince", "Splendid"]
brands_high_end = ["Chanel", "Dior", "Gucci", "Prada", "Louis Vuitton", "Hermès", "Givenchy"]
brands_affordable = ["Old Navy", "H&M", "Zara", "Uniqlo", "Gap", "Forever 21", "Target"]
product_names_apparel = ["Cotton T-Shirt", "Skinny Jeans", "Hooded Jacket", "Summer Dress", "Yoga Pants"]
product_names_beauty = ["Moisturizing Cream", "Shampoo", "Lipstick", "Foundation", "Highlighter"]
materials = ["100% Cotton", "Cotton/Polyester Blend", "100% Polyester", "Wool Blend", "Nylon/Spandex"]
fits = ["Regular", "Slim", "Loose", "Fitted"]
perceived_values = [3, 4, 5]
durabilities = [3, 4, 5]
skin_types = ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
hair_types = ["Straight", "Wavy", "Curly", "Coily"]
ratings = [1, 2, 3, 4, 5]
descriptions = [
    "A high-quality product that meets all your needs.",
    "Designed for comfort and style.",
    "Perfect for everyday use.",
    "A must-have in your wardrobe.",
    "Provides excellent results and satisfaction."
]
genders = ["Men", "Women", "Unisex"]
activity_types = ["Casual", "Formal", "Active"]

# Function to generate a random product
def generate_product(index):
    category = random.choice(apparel_categories + beauty_categories)
    if category in apparel_categories:
        sub_category = category
        brand = random.choice(brands_mid_range + brands_high_end + brands_affordable)
        product_name = random.choice(product_names_apparel)
        product_attributes = {
            "fit": random.choice(fits),
            "material": random.choice(materials),
            "perceivedValue": random.choice(perceived_values),
            "durability": random.choice(durabilities)
        }
        skin_type = None
        hair_type = None
    else:
        sub_category = category
        brand = random.choice(brands_high_end + brands_affordable)
        product_name = random.choice(product_names_beauty)
        product_attributes = {
            "fit": None,
            "material": None,
            "perceivedValue": random.choice(perceived_values),
            "durability": random.choice(durabilities)
        }
        skin_type = random.choice(skin_types) if category == "Skincare" else None
        hair_type = random.choice(hair_types) if category == "Haircare" else None
    
    product_price = round(random.uniform(10, 500), 2)
    product_page_link = f"https://example.com/product{index}"
    product_images = [f"https://example.com/product{index}-image1.jpg", f"https://example.com/product{index}-image2.jpg"]
    customer_reviews = ["Great product!", "Very comfortable.", "High quality.", "Would buy again."]
    product_rating = random.choice(ratings)
    product_description = random.choice(descriptions)
    product_gender = random.choice(genders)
    activity_type = random.choice(activity_types)
    
    return {
        "category": "Apparel" if category in apparel_categories else "Beauty",
        "subCategory": sub_category,
        "brand": brand,
        "productPageLink": product_page_link,
        "productName": product_name,
        "productPrice": product_price,
        "productImages": product_images,
        "customerReviews": customer_reviews,
        "productAttributes": product_attributes,
        "productRating": product_rating,
        "productDescription": product_description,
        "skinType": skin_type,
        "hairType": hair_type,
        "productGender": product_gender,
        "activityType": activity_type
    }

# Generate 10,000 products
products = [generate_product(i) for i in range(1, 10001)]

# Write to JSON file
with open('realistic_products.json', 'w') as f:
    json.dump(products, f, indent=4)

print("JSON file with 10,000 realistic products has been generated.")