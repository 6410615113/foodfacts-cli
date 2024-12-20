import os
import json
import requests

FAVORITES_FILE = "favorites.json"
API_URL = "https://world.openfoodfacts.org/api/v2/product/{product_id}.json"

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_favorite(favorites):
    with open(FAVORITES_FILE, "w") as file:
        json.dump(favorites, file, indent=4)


def fetch_product_name(product_id):
    try:
        response = requests.get(API_URL.format(product_id=product_id))
        if response.status_code == 200:
            data = response.json()
            product_name = data.get("product", {}).get("product_name", "Unknown Product")
            return product_name
        else:
            return "Unknown Product"
    except requests.RequestException:
        return "Error fetching product"


def register_command(subparsers):
    parser = subparsers.add_parser("favorites", help="Display or manage favorite products")
    subparsers_favorites = parser.add_subparsers(dest="action", help="Favorites actions")

    add_parser = subparsers_favorites.add_parser("add", help="Add a product to favorites")
    add_parser.add_argument("product_id", help="The ID of the product to add")

    list_parser = subparsers_favorites.add_parser("list", help="List all favorite products")

    remove_parser = subparsers_favorites.add_parser("remove", help="Remove a product from favorites")
    remove_parser.add_argument("product_id", help="The ID of the product to remove")

    parser.set_defaults(func=execute)


def execute(args):
    favorites = load_favorites()

    if args.action == "add":
        if args.product_id in favorites:
            print(f"Product {args.product_id} is already in favorites.")
        else:
            favorites.append(args.product_id)
            save_favorite(favorites)
            print(f"Product {args.product_id} added to favorites.")

    elif args.action == "list":
        if favorites:
            print("Your favorite products:")
            for product_id in favorites:
                product_name = fetch_product_name(product_id)
                print(f"- {product_name} (ID: {product_id})")
        else:
            print("You have no favorite products.")

    elif args.action == "remove":
        if args.product_id in favorites:
            favorites.remove(args.product_id)
            save_favorite(favorites)
            print(f"Product {args.product_id} removed from favorites.")
        else:
            print(f"Product {args.product_id} is not in favorites.")
    else:
        print("Invalid action. Use 'add', 'list', or 'remove'.")
