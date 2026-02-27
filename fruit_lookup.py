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

    nutritions = raw.get("nutritions", {})

    return {
        "name": raw.get("name"),
        "id": raw.get("id"),
        "family": raw.get("family"),
        "sugar": raw.get("sugar"),
        "carbohydrates": raw.get("carbohydrates"),

    }

