import requests

def register_command(subparsers):
    parser = subparsers.add_parser("allergy", help="Check for products with a specific allergen")
    parser.add_argument("allergen", type=str, help="The allergen to search for (e.g., gluten, nuts, milk)")
    parser.set_defaults(func=execute)

def execute(args):
    allergen = args.allergen
    print(f"Searching for products with allergen: {allergen}...")
    
    # API endpoint for allergen search
    url = f"https://world.openfoodfacts.org/allergen/{allergen}.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            
            if not products:
                print(f"No products found with the allergen: {allergen}.")
                return
            
            print(f"Found {len(products)} products with the allergen: {allergen} (Showing up to 10):")
            for i, product in enumerate(products[:10], 1):  # Limit to 10 results
                name = product.get("product_name", "Unknown")
                brand = product.get("brands", "Unknown")
                print(f"{i}. {name} (Brand: {brand})")
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
