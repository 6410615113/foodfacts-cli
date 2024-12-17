# FoodFacts CLI
A command-line tool to interact with the Open Food Facts API.

## Features
- `help`: Display available subcommands.
- `list`: List available data categories.
- `search <category>`: Display all Product Name and Product ID (barcode) in category. 

## `Dockerfile` usage
1. Build the Docker container: 
```console
docker image build --tag foodfacts .
```
2. Run the application: 
```console
docker container run -d foodfacts-cli
```
3. Commmand to use `help` subcommand:
```console
docker container run foodfacts-cli python foodfacts/cli.py help
```
3. Commmand to use `list` subcommand:
```console
docker container run foodfacts-cli python foodfacts/cli.py list
```
4. Commmand to use `search` subcommand:
```console
docker container run foodfacts-cli python foodfacts/cli.py search <category>
```

## `compose.yml` usage
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
4. Commmand to use `search` subcommand:
```console
docker compose run foodfacts-cli python foodfacts/cli.py search <category>
```
