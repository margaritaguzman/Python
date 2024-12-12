import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from analysis import analyze_recipes


class TestAnalysis(unittest.TestCase):
    # Mock the database connection and query
    @patch('sqlite3.connect')
    def test_analyze_recipes_db_query(self, mock_connect):
        # Simulate database connection and returned data
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Simulate the data returned by pd.read_sql_query
        sample_data = pd.DataFrame({
            'ingredients': ['2 eggs, 1 cup milk', '1 cup sugar', '2 eggs, 1/2 cup sugar'],
            'time': [30, 45, 25]
        })
        with patch('pandas.read_sql_query', return_value=sample_data) as mock_query:
            # Call the function under test
            with patch('matplotlib.pyplot.show') as mock_show:
                analyze_recipes()
                
                # Ensure database query is called
                mock_query.assert_called_once()
                # Check matplotlib's `plt.show()` is called to visualize plots
                mock_show.assert_called()

    # Mock the ingredient counts
    @patch('matplotlib.pyplot.show')
    @patch('sqlite3.connect')
    def test_plot_ingredient_counts(self, mock_connect, mock_show):
        # Simulate database connection and returned data
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        sample_data = pd.DataFrame({
            'ingredients': ['egg', 'milk', 'sugar', 'egg', 'sugar', 'egg'],
            'time': [30, 20, 15, 25, 10, 20]
        })
        with patch('pandas.read_sql_query', return_value=sample_data):
            # Call analyze_recipes
            analyze_recipes()
            mock_show.assert_called()


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
