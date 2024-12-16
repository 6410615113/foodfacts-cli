import requests

def register_command(subparsers):
    parser = subparsers.add_parser("list", help="List available data categories")
    parser.set_defaults(func=execute)

def execute(args):
    url = "https://world.openfoodfacts.org/categories.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print("Raw Response Content:")
            # print(response.text)
            try:
                data = response.json()
                categories = data.get("tags", [])
                if categories:
                    print("Available data categories:")
                    for category in categories[:10]:
                        print(f"- {category.get('name', 'Unknown')}")
                else:
                    print("No categories found.")
            except requests.exceptions.JSONDecodeError:
                print("Failed to parse JSON response. The API returned invalid data.")
                print(f"Response Content: {response.text}")
        else:
            print(f"Failed to fetch categories. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
