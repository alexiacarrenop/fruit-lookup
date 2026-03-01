"""
fruit_lookup.py - Fetch nutritional data from the FruityVice API.

Run from the command line or import as a library.

Examples(human-readable and machine-readable):
    python fruit_lookup.py strawberry
    python fruit_lookup.py banana --format machine

"""

import sys
import json
import argparse
import requests

API_URL = "https://www.fruityvice.com/api/fruit"

def get_fruit(name):
    """
    Fetch data from FruityVice API.

    Args:
        name: A string. The name of the fruit, e.g. "strawberry"

    Returns:
        A dict with keys: name, id, family, sugar, carbohydrates

    Raises:
          ValueError: If the fruit is not found or name is empty.
          ConnectionError: If API can't be reached

    """
    if not name or not name.strip():
        raise ValueError("Fruit name can't be empty")

    url = f"{API_URL}/{name.strip().lower()}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Could not reach the FruityVice API. "
            "Please check your internet connection."
        )
    except requests.exceptions.Timeout:
        raise ConnectionError(
            "Request timed out. FruityVice API may not be available."
        )

    if response.status_code == 404:
        raise ValueError(
            f"Fruit '{name}' was not found. Check the spelling and try again."
        )
    if not response.ok:
        raise ConnectionError(
            f"Unexpected error (HTTP {response.status_code})."
        )

    raw = response.json() #parse into a python dict

    nutritions = raw.get("nutritions", {})

    return {
        "name": raw.get("name"),
        "id": raw.get("id"),
        "family": raw.get("family"),
        "sugar": nutritions.get("sugar"),
        "carbohydrates": nutritions.get("carbohydrates"),
    }


def format_human(fruit: dict) -> str:
    """Format data into a human-readable output"""
    return (
        f"Fruit: {fruit['name']}\n"
        f"ID: {fruit['id']}\n"
        f"Family: {fruit['family']}\n"
        f"Sugar: {fruit['sugar']} g\n"
        f"Carbohydrates: {fruit['carbohydrates']} g"
        )

def format_machine(fruit: dict) -> str:
    """Format data as machine-readable JSON output"""
    return json.dumps(fruit, indent=2) #convert python dict into json string

def build_parser():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="fruit_lookup",
        description="Look up nutritional information for a fruit on FruityVice."
    )
    parser.add_argument(
        "fruit",
        help="Name of the fruit to look up (e.g. strawberry)"
    )
    parser.add_argument(
        "--format",
        choices=["human","machine"],
        default="human",
        help="Output format: 'human' (default) or 'machine' (json)."
    )
    return parser


def main(argv=None):
    """"""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        fruit = get_fruit(args.fruit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    except ConnectionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.format == "machine":
        print(format_machine(fruit))
    else:
        print(format_human(fruit))


if __name__ == "__main__":
    main()



