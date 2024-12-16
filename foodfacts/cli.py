import argparse
from foodfacts.commands import help, list, get_product
import sys
print("Python Path:", sys.path)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    help.register_command(subparsers)
    list.register_command(subparsers)
    get_product.register_command(subparsers)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
