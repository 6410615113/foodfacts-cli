import requests
from tabulate import tabulate

def register_command(subparsers):
    get_product_parser = subparsers.add_parser('search')
    get_product_parser.add_argument('category')
    get_product_parser.set_defaults(func=execute)

def execute(args):
    category = args.category
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={category}&action=process&json=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            table_data = []
            for product in products:
                product_name = product.get('product_name', 'N/A')
                product_id = product.get('code', 'N/A')
                table_data.append([product_name, product_id])

            print(f"Found {len(products)} products:")
            headers = ["Product Name", "Product ID"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"No products found for category '{category}'.")
    else:
        print(f"Failed to fetch products for category '{category}'. HTTP Status Code: {response.status_code}")