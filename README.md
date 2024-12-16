# FoodFacts CLI
A command-line tool to interact with the Open Food Facts API.

## Features
- `help`: Display available subcommands.
- `list`: List available data categories.


## Usage
1. Build the Docker container: 
```console
docker-compose build
```
2. Run the application: 
```console
docker-compose up
```
3. Commmand to use `help` subcommand:
```console
docker-compose run foodfacts-cli python foodfacts/cli.py help
```
3. Commmand to use `list` subcommand:
```console
docker-compose run foodfacts-cli python foodfacts/cli.py list
```