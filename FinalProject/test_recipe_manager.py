import unittest
import re
from unittest.mock import patch, MagicMock
import recipe_manager
import database


class TestRecipeManager(unittest.TestCase):
    
    # Test title validation
    def test_validate_title_valid(self):
        self.assertTrue(recipe_manager.validate_title("Chicken Pasta"))
    
    def test_validate_title_invalid(self):
        self.assertFalse(recipe_manager.validate_title("Chicken@Pasta"))
    
    # Test ingredients validation
    def test_validate_ingredients_valid(self):
        self.assertTrue(recipe_manager.validate_ingredients("2 eggs, 1 cup milk, 1/2 cup sugar"))
    
    def test_validate_ingredients_invalid(self):
        self.assertFalse(recipe_manager.validate_ingredients("2eggs milk sugar"))
    
    # Test instructions validation
    def test_validate_instructions_valid(self):
        self.assertTrue(recipe_manager.validate_instructions("Boil water and add pasta."))
    
    def test_validate_instructions_invalid(self):
        self.assertFalse(recipe_manager.validate_instructions("Boil@water!"))
    
    # Test cooking time validation
    def test_validate_cooking_time_valid(self):
        self.assertTrue(recipe_manager.validate_cooking_time("30"))
    
    def test_validate_cooking_time_invalid(self):
        self.assertFalse(recipe_manager.validate_cooking_time("-10"))



     # Regex-based normalization function for comparison
    def normalize_sql(self, sql_query):
        # Replace multiple spaces with a single space and remove leading/trailing whitespace
        return re.sub(r'\s+', ' ', sql_query).strip()
    
    # Test add_recipe_ui (mock database call)
    @patch('database.add_to_db')
    def test_add_recipe_ui_valid_input(self, mock_add_to_db):
        with patch('builtins.input', side_effect=["Pasta", "2 eggs, 1 cup milk", "Boil for 30 mins", "30", "Dinner"]):
            recipe_manager.add_recipe_ui()
            mock_add_to_db.assert_called_once_with(
                "Pasta", "2 eggs, 1 cup milk", "Boil for 30 mins", 30, "Dinner"
            )
    
    # Test delete_recipe_ui with valid input
    @patch('database.delete_recipe')
    def test_delete_recipe_ui_valid_input(self, mock_delete_recipe):
        with patch('builtins.input', return_value="1"):
            recipe_manager.delete_recipe_ui()
            mock_delete_recipe.assert_called_once_with(1)
    
    # Test delete_recipe_ui with invalid input
    @patch('database.delete_recipe')
    def test_delete_recipe_ui_invalid_input(self, mock_delete_recipe):
        with patch('builtins.input', return_value="abc"):
            recipe_manager.delete_recipe_ui()
            mock_delete_recipe.assert_not_called()
    
    # Test update_recipe_ui with valid user input
    @patch('sqlite3.connect')
    def test_update_recipe_ui_valid_input(self, mock_sqlite_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with patch('builtins.input', side_effect=["1", "Pasta", "2 eggs, 1 cup milk", "Boil for 30 mins", "30", "Dinner"]):
            recipe_manager.update_recipe_ui()

            # Normalize expected and actual SQL strings
            expected_query = '''
                UPDATE recipes 
                SET title = ?, ingredients = ?, instructions = ?, time = ?, category = ?
                WHERE id = ?
            '''
            actual_query = mock_cursor.execute.call_args[0][0]

            # Normalize both for comparison
            expected_query_normalized = self.normalize_sql(expected_query)
            actual_query_normalized = self.normalize_sql(actual_query)

            # Compare the cleaned query strings
            self.assertEqual(expected_query_normalized, actual_query_normalized)

            # Assert execution and commit
            mock_cursor.execute.assert_called_once()
            mock_conn.commit.assert_called_once()
    
    # Test search_recipe_ui with valid mock database response
    @patch('database.fetch_recipe_by_title')
    def test_search_recipe_ui_valid(self, mock_fetch_recipe_by_title):
        mock_fetch_recipe_by_title.return_value = [
            (1, "Pasta", "2 eggs, 1 cup milk", "Boil for 30 mins", 30, "Dinner")
        ]
        
        with patch('builtins.input', return_value="Pasta"):
            with patch('builtins.print') as mock_print:
                recipe_manager.search_recipe_ui()
                mock_print.assert_any_call("\nFound recipes:")
                mock_print.assert_any_call(
                    "ID: 1\nTitle: Pasta\nIngredients: 2 eggs, 1 cup milk\nInstructions: Boil for 30 mins\nCooking Time: 30 minutes\nCategory: Dinner"
                )


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
