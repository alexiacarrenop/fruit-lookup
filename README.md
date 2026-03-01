# fruit_lookup

A Python command-line tool and library for searching nutritional data from the [FruityVice API](https://www.fruityvice.com/).

## Features

- Look up any fruit by name
- Two output formats: human-readable and machine-readable (JSON)
- Graceful error handling for unknown fruits and API errors
- Works as a CLI tool **and** as an importable Python library
- Easy to extend with new output formats or data sources

## Requirements

- Python 3.8+
- [requests](https://pypi.org/project/requests/)

## Installation

```bash
git clone https://github.com/alexiacarrenop/fruit-lookup
cd fruit-lookup
pip install -r requirements.txt
```

## CLI Usage

```bash
# Human-readable output (default)
python fruit_lookup.py strawberry

# Machine-readable output
python fruit_lookup.py banana --format machine

# Error handling: unknown fruit
python fruit_lookup.py wineberry

# Error handling: misspelled fruit
python fruit_lookup.py bannanna
```

### Example output (human)

```
Fruit:          Strawberry
ID:             3
Family:         Rosaceae
Sugar:          4.89 g
Carbohydrates:  7.68 g
```

### Example output (machine)

```json
{
  "name": "Strawberry",
  "id": 3,
  "family": "Rosaceae",
  "sugar": 4.89,
  "carbohydrates": 7.68
}
```

## Library Usage

```python
from fruit_lookup import get_fruit, format_human, format_machine

# Fetch data (raises ValueError or ConnectionError on failure)
fruit = get_fruit("strawberry")

# Format it
print(format_human(fruit))
print(format_machine(fruit))

# Or work with the raw dict directly
print(fruit["sugar"])
```

## Project Structure

```
fruit_lookup.py   # main file with library functions
requirements.txt  # Python dependencies
README.md         # this file
```