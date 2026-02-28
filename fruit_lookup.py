#!/usr/bin/env python3

"""
main docstring
"""

import sys
import json
import argparse
import requests







API_URL = "https://www.fruityvice.com/api/fruit"

def get_fruit(name: str) -> dict:
    """
    Fetch data from FruityVice API.

    Args:
        name: The name of the fruit, e.g. "strawberry"

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

    raw = response.json()
    if response.status_code == 404:
        raise ValueError(
            f"Fruit '{name}' was not found."
        )

    if not response.ok:
        raise ConnectionError(
            f"Unexpected API error (HTTP {response.status_code})."
        )

    nutritions = raw.get("nutritions", {})

    return {
        "name": raw.get("name"),
        "id": raw.get("id"),
        "family": raw.get("family"),
        "sugar": nutritions.get("sugar"),
        "carbohydrates": nutritions.get("carbohydrates"),
    }


def format_human(fruit: dict) -> str:
    """Format data into human-readable output"""
    return (
        f"Fruit: {fruit['name']}\n"
        f"ID: {fruit['id']}\n"
        f"Family: {fruit['family']}\n"
        f"Sugar: {fruit['sugar']} g\n"
        f"Carbohydrates: {fruit['carbohydrates']} g"
        )

def format_json(fruit: dict) -> str:
    """Format data as machine-readable JSON output"""
    return json.dumps(fruit, indent=2)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fruit_lookup",
    )
    parser.add_argument(
        "fruit",
    )
    parser.add_argument(
        "--format",
        choices=["human","machine"],
        default="human",
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
        print(format_json(fruit))
    else:
        print(format_human(fruit))


if __name__ == "__main__":
    main()



