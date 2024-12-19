def register_command(subparsers):
    parser = subparsers.add_parser("help", help="Display available commands")
    parser.set_defaults(func=execute)

def execute(args):
    commands = {
        "help": "Display available commands",
        "list": "List available data categories",
        "search <category>": "Display all Product Name and Product ID (barcode) in category",
        "nutritions <product_id>": "Display nutrition facts of products",
    }

    print("Available commands:")
    for command, description in commands.items():
        print(f"- {command}: {description}")
