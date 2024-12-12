import unittest
import database
import sqlite3


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Prepare the database for each test - recreate the database
        database.create_database()
        # Clear any existing data
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes")
        conn.commit()
        conn.close()

    def test_add_and_fetch_all_recipes(self):
        # Add recipes to database
        database.add_to_db('Pasta', 'noodles, tomato', 'cook for 20 min', 30, 'main')
        database.add_to_db('Cake', 'flour, sugar', 'bake for 30 min', 45, 'dessert')

        # Fetch all recipes
        recipes = database.fetch_all_recipes()
        self.assertEqual(len(recipes), 2)  # Ensure two recipes are fetched
        self.assertTrue(any(recipe[1] == 'Pasta' for recipe in recipes))
        self.assertTrue(any(recipe[1] == 'Cake' for recipe in recipes))

    def test_fetch_by_title(self):
        # Add recipes to database
        database.add_to_db('Pasta', 'noodles, tomato', 'cook for 20 min', 30, 'main')
        database.add_to_db('Cake', 'flour, sugar', 'bake for 30 min', 45, 'dessert')

        # Search by title
        recipes_pasta = database.fetch_recipe_by_title('Pasta')
        recipes_cake = database.fetch_recipe_by_title('Cake')
        self.assertEqual(len(recipes_pasta), 1)
        self.assertEqual(recipes_pasta[0][1], 'Pasta')
        self.assertEqual(len(recipes_cake), 1)
        self.assertEqual(recipes_cake[0][1], 'Cake')

    def test_delete_recipe(self):
        # Add recipes to database
        database.add_to_db('Pasta', 'noodles, tomato', 'cook for 20 min', 30, 'main')
        database.add_to_db('Cake', 'flour, sugar', 'bake for 30 min', 45, 'dessert')

        # Fetch initial state
        recipes = database.fetch_all_recipes()
        self.assertEqual(len(recipes), 2)

        # Delete the first recipe by ID
        recipe_id_to_delete = recipes[0][0]  # Get the ID of the first recipe
        database.delete_recipe(recipe_id_to_delete)

        # Fetch recipes again
        updated_recipes = database.fetch_all_recipes()
        self.assertEqual(len(updated_recipes), 1)  # Only one recipe should remain
        self.assertFalse(any(recipe[0] == recipe_id_to_delete for recipe in updated_recipes))


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)