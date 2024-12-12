import re
import database
from database import create_database
import sqlite3


# Validation functions using regex
def validate_title(title):
    pattern = r"^[a-zA-Z0-9\s\-\.,'!]+$"
    return bool(re.match(pattern, title))

def validate_ingredients(ingredients):
    # Validates comma-separated ingredients (e.g., "2 eggs, 1 cup milk, 1/2 cup sugar")
    pattern = r"^(\d+(/\d+)?\s[a-zA-Z]+(\s[a-zA-Z]+)*)(,\s*\d+(/\d+)?\s[a-zA-Z]+(\s[a-zA-Z]+)*)*$"
    return bool(re.match(pattern, ingredients))

def validate_instructions(instructions):
    pattern = r"^[a-zA-Z0-9\s\-\.,'!]+$"
    return bool(re.match(pattern, instructions))

def validate_cooking_time(time):
    pattern = r"^\d+$"  # Matches only numeric input for time in minutes
    return bool(re.match(pattern, time))


# Validations before adding a recipe
def add_recipe_ui():
    print("\nAdd a new recipe:")
    title = input("Recipe title: ")
    if not validate_title(title):
        print("Invalid title. Please use letters, numbers, spaces, and basic punctuation.")
        return
    ingredients = input("Ingredients (comma-separated): ")
    if not validate_ingredients(ingredients):
        print("Invalid ingredients format. Use 'quantity unit ingredient' format, separated by commas.")
        return
    instructions = input("Instructions: ")
    if not validate_instructions(instructions):
        print("Invalid instructions. Please use letters, numbers, spaces, and basic punctuation.")
        return
    time = input("Cooking time (in minutes): ")
    if not validate_cooking_time(time):
        print("Invalid cooking time. Please enter a numeric value.")
        return
    category = input("Category (e.g., Breakfast, Lunch, Dinner): ")
    database.add_to_db(
        title, ingredients, instructions, int(time), category
    )
    print("Recipe added successfully!")

# Search for the recipe using title or keyword
def search_recipe_ui():
    search_term = input("\nEnter the recipe title or keyword to search: ")
    recipes = database.fetch_recipe_by_title(search_term)
    if recipes:
        print("\nFound recipes:")
        for recipe in recipes:
            print(
                f"ID: {recipe[0]}\nTitle: {recipe[1]}\nIngredients: {recipe[2]}\nInstructions: {recipe[3]}\nCooking Time: {recipe[4]} minutes\nCategory: {recipe[5]}"
            )
    else:
        print("No recipes found.")

# delete the recipe
def delete_recipe_ui():
    print("\nDelete a recipe:")
    recipe_id = input("Enter the recipe ID to delete: ")
    if recipe_id.isdigit():
        database.delete_recipe(int(recipe_id))
        print("Recipe deleted.")
    else:
        print("Invalid input. Recipe not deleted.")

# Update existing recipe
def update_recipe_ui():
    recipe_id = input("\nEnter the recipe ID to update: ")
    if not recipe_id.isdigit():
        print("Invalid ID.")
        return

    recipe_id = int(recipe_id)
    new_title = input("New title: ")
    if not validate_title(new_title):
        print("Invalid title. Update aborted.")
        return
    new_ingredients = input("New ingredients: ")
    if not validate_ingredients(new_ingredients):
        print("Invalid ingredients format. Update aborted.")
        return
    new_instructions = input("New instructions: ")
    if not validate_instructions(new_instructions):
        print("Invalid instructions. Update aborted.")
        return
    new_time = input("New cooking time: ")
    if not validate_cooking_time(new_time):
        print("Invalid time. Update aborted.")
        return
    new_category = input("New category: ")


    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE recipes 
        SET title = ?, ingredients = ?, instructions = ?, time = ?, category = ?
        WHERE id = ?
    ''', (new_title, new_ingredients, new_instructions, int(new_time), new_category, recipe_id))
    conn.commit()
    conn.close()
    print("Recipe updated successfully!")
