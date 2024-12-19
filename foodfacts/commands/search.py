import requests
from tabulate import tabulate

def register_command(subparsers):
    get_product_parser = subparsers.add_parser('search', help="Search products by category or ID")
    get_product_parser.add_argument('query', help="Category name or Product ID to search")
    get_product_parser.set_defaults(func=execute)

def execute(args):
    query = args.query

    if query.isdigit():  # Check if the input is a numeric product ID
        url = f"https://world.openfoodfacts.org/api/v0/product/{query}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'product' in data:
                product = data['product']
                # Display detailed product information
                table_data = [
                    ["Product Name", product.get('product_name', 'N/A')],
                    ["Brand", product.get('brands', 'N/A')],
                    ["Nutritional Grade", product.get('nutrition_grades', 'N/A')],
                    ["Energy (kcal)", product.get('nutriments', {}).get('energy-kcal_100g', 'N/A')],
                    ["Proteins (g)", product.get('nutriments', {}).get('proteins_100g', 'N/A')],
                    ["Carbohydrates (g)", product.get('nutriments', {}).get('carbohydrates_100g', 'N/A')],
                    ["Fat (g)", product.get('nutriments', {}).get('fat_100g', 'N/A')]
                ]
                print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
            else:
                print(f"No detailed information available for product ID '{query}'.")
        else:
            print(f"Failed to fetch product details for ID '{query}'. HTTP Status Code: {response.status_code}")
    else:
        # Search by category
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&action=process&json=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            if products:
                table_data = []
                for product in products[:10]:  # Limit to first 10 results
                    product_name = product.get('product_name', 'N/A')
                    product_id = product.get('code', 'N/A')
                    table_data.append([product_name, product_id])

                print(f"Found {len(products)} products:")
                headers = ["Product Name", "Product ID"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print(f"No products found for category '{query}'.")
        else:
            print(f"Failed to fetch products for category '{query}'. HTTP Status Code: {response.status_code}")
