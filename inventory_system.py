"""
Inventory Management System

This module provides functions to manage inventory items including
adding, removing, loading, saving, and reporting on stock levels.
"""

import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory.

    Args:
        item (str): Name of the item to add
        qty (int): Quantity to add
        logs (list): Optional list to append log entries to

    Returns:
        None
    """
    if logs is None:
        logs = []

    if not item or not isinstance(item, str):
        return

    if not isinstance(qty, int) or qty < 0:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Remove an item from the inventory.

    Args:
        item (str): Name of the item to remove
        qty (int): Quantity to remove

    Returns:
        None
    """
    try:
        if item not in stock_data:
            print(f"Warning: Item '{item}' not found in inventory")
            return

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except (KeyError, TypeError) as e:
        print(f"Error removing item '{item}': {e}")


def get_qty(item):
    """
    Get the quantity of an item in inventory.

    Args:
        item (str): Name of the item

    Returns:
        int: Quantity of the item, or 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: File '{file}' not found. "
              "Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{file}': {e}")
        stock_data = {}


def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
    except IOError as e:
        print(f"Error saving data to '{file}': {e}")


def print_data():
    """
    Print the current inventory report.

    Returns:
        None
    """
    print("Items Report")
    for item in stock_data:
        print(f"{item} -> {stock_data[item]}")


def check_low_items(threshold=5):
    """
    Check for items below a quantity threshold.

    Args:
        threshold (int): Minimum quantity threshold

    Returns:
        list: List of items below the threshold
    """
    result = []
    for item in stock_data:
        if stock_data[item] < threshold:
            result.append(item)
    return result


def main():
    """
    Main function to demonstrate inventory system functionality.

    Returns:
        None
    """
    add_item("apple", 10)
    add_item("banana", 5)
    # Invalid type handling - now properly validated
    add_item(123, "ten")  # Will be rejected by type checking
    remove_item("apple", 3)
    remove_item("orange", 1)  # Will show warning
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()
    # Removed dangerous eval() call
    print("Inventory operations completed successfully")


if __name__ == "__main__":
    main()