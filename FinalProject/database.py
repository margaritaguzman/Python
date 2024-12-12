import sqlite3

# Create the database schema
def create_database():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            time INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add recipes to the database
def add_to_db(title, ingredients, instructions, time, category):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (title, ingredients, instructions, time, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, ingredients, instructions, time, category))
    conn.commit()
    conn.close()

# Find all recipes
def fetch_all_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

#Find recipe by title
def fetch_recipe_by_title(title):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE title LIKE ?", (f'%{title}%',))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

# Delete recipe
def delete_recipe(recipe_id):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()

# for testing purposes only
#def add_to_db(*args):
    #pass  # Mock database interaction for adding recipes.
# for testing purposes only
#def fetch_recipe_by_title(search_term):
    #return []  # Simulate database response
# for testing purposes only
#def delete_recipe(recipe_id):
   # pass  # Mock database delete
