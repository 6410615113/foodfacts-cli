# FoodFacts CLI
A command-line tool to interact with the Open Food Facts API.

## Features
- `help`: Display available subcommands.
- `list`: List available data categories.
- `get_product <category>`: Display all Product Name and Product ID (barcode) in category. 


## Usage
1. Build the Docker container: 
```console
docker compose build
```
2. Run the application: 
```console
docker compose up --detach
```
3. Commmand to use `help` subcommand:
```console
docker compose run foodfacts-cli python foodfacts/cli.py help
```
3. Commmand to use `list` subcommand:
```console
docker compose run foodfacts-cli python foodfacts/cli.py list
```
4. Commmand to use `get_product` subcommand:
```console
docker compose run foodfacts-cli python foodfacts/cli.py get_product <category>
```
