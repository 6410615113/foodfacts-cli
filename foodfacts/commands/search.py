import requests
import textwrap
from tabulate import tabulate

def register_command(subparsers):
    search_parser = subparsers.add_parser('search', help="Search for a product by category or ID")
    search_parser.add_argument('query', help="Category name or Product ID to search")
    search_parser.set_defaults(func=execute)

def format_text(label, text, width=70):
    if text != 'N/A':
        wrapped_text = textwrap.fill(text, width=width, subsequent_indent='                                 ')
    else:
        wrapped_text = 'N/A'
    return f"{label:<31}: {wrapped_text}"

def execute(args):
    query = args.query

    if query.isdigit():
        url = f"https://world.openfoodfacts.org/api/v0/product/{query}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'product' in data:
                product = data['product']
                print(f"\n{product.get('product_name', 'N/A')} - "
                      f"{product.get('brands', 'N/A')} - {product.get('quantity', 'N/A')}\n")
                
                print("Product Details:")
                barcode_number = product.get('code', 'N/A')
                print(format_text("Barcode", barcode_number))
                print(format_text("Common name", product.get('generic_name', 'N/A')))
                print(format_text("Quantity", product.get('quantity', 'N/A')))
                print(format_text("Packaging", product.get('packaging', 'N/A')))
                print(format_text("Brands", product.get('brands', 'N/A')))
                print(format_text("Categories", product.get('categories', 'N/A')))
                print(format_text("Labels, certifications, awards", product.get('labels', 'N/A')))
                print(format_text("Origin", product.get('origins', 'N/A')))
                print(format_text("Manufacturing/Processing places", product.get('manufacturing_places', 'N/A')))
                print(format_text("Stores", product.get('stores', 'N/A')))
                print(format_text("Countries where sold", product.get('countries', 'N/A')))
                print(format_text("Link to the product page", product.get('url', 'N/A')))
            else:
                print(f"No detailed information available for product ID '{query}'.")
        else:
            print(f"Failed to fetch product details for ID '{query}'. HTTP Status Code: {response.status_code}")
    else:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&action=process&json=true"
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
                print(f"No products found for category '{query}'.")
        else:
            print(f"Failed to fetch products for category '{query}'. HTTP Status Code: {response.status_code}")
