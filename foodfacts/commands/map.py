import requests
import os

OPENCAGE_API_KEY = "724912952d4e44c6a365265568d7ee3a"

def register_command(subparsers):
    get_product_parser = subparsers.add_parser('map')
    get_product_parser.add_argument('category')
    get_product_parser.set_defaults(func=execute)

def execute(args):
    category = args.category
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={category}&action=process&json=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        create_map(data, category)
    else:
        print("Failed to retrieve data")

def get_coordinates_with_opencage(location_name):
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location_name,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            geometry = data['results'][0]['geometry']
            return [geometry['lat'], geometry['lng']]
    return None

def create_map(data, category):
    products = data.get('products', [])
    if not products:
        print("No products found")
        return

    markers = []
    map_center = [48.8566, 2.3522]

    for product in products:
        product_name = product.get('product_name', 'Unknown Product')
        manufacturing_places = product.get('manufacturing_places', None)
        manufacturing_places_tags = product.get('manufacturing_places_tags', [])

        places = manufacturing_places_tags if manufacturing_places_tags else (
            [manufacturing_places] if manufacturing_places else []
        )

        for place in places:
            coordinates = get_coordinates_with_opencage(place)
            if coordinates:
                markers.append({
                    "name": product_name,
                    "place": place,
                    "latitude": coordinates[0],
                    "longitude": coordinates[1]
                })
                if map_center == [48.8566, 2.3522]:  # เปลี่ยน map center ถ้ายังเป็นค่าเริ่มต้น
                    map_center = coordinates

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Map</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <style>
            #map {{ height: 100vh; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView({map_center}, 5);

            // Add OpenStreetMap tiles
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19
            }}).addTo(map);

            // Add markers
            var markers = {markers};
            markers.forEach(function(marker) {{
                L.marker([marker.latitude, marker.longitude]).addTo(map)
                    .bindPopup(`<b>${{marker.name}}</b><br>${{marker.place}}`);
            }});
        </script>
    </body>
    </html>
    """

    save_dir = os.path.join(os.getcwd(), 'maps')
    os.makedirs(save_dir, exist_ok=True)
    
    map_path = os.path.join(save_dir, f'category_{category}_map.html')
    try:
        with open(map_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Map saved to {map_path}")
    except Exception as e:
        print(f"Failed to save map: {e}")