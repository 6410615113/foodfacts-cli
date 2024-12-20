import requests
from tabulate import tabulate

def register_command(subparsers):
    get_product_parser = subparsers.add_parser('nutrition', help="Display nutrition facts of products")
    get_product_parser.add_argument('product_id')
    get_product_parser.set_defaults(func=execute)

def execute(args):
    product_id = args.product_id
    url = f"https://world.openfoodfacts.org/api/v0/product/{product_id}.json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        show_nutrition_facts(data)
    else:
        print("Failed to retrieve data")

def show_nutrition_facts(data):
    product = data.get('product', {})
    if not product:
        print("No product found")
        return

    product_name = product.get('product_name', 'N/A')
    nutriments = product.get('nutriments', {})
    energy = nutriments.get('energy-kcal_100g', 'N/A')
    fat = nutriments.get('fat_100g', 'N/A')
    saturated_fat = nutriments.get('saturated-fat_100g', 'N/A')
    carbohydrates = nutriments.get('carbohydrates_100g', 'N/A')
    sugars = nutriments.get('sugars_100g', 'N/A')
    fiber = nutriments.get('fiber_100g', 'N/A')
    proteins = nutriments.get('proteins_100g', 'N/A')
    salt = nutriments.get('salt_100g', 'N/A')

    nutrition_facts = [
        ["Product Name", product_name],
        ["Energy (kcal/100g)", energy],
        ["Fat (g/100g)", fat],
        ["Saturated Fat (g/100g)", saturated_fat],
        ["Carbohydrates (g/100g)", carbohydrates],
        ["Sugars (g/100g)", sugars],
        ["Fiber (g/100g)", fiber],
        ["Proteins (g/100g)", proteins],
        ["Salt (g/100g)", salt],
    ]

    print(tabulate(nutrition_facts, tablefmt="grid"))