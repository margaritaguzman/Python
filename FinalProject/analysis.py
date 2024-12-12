import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


def analyze_recipes():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query('SELECT * FROM recipes', conn)

    # Ingredient Frequency Analysis
    ingredients = df['ingredients'].str.split(',').explode()
    ingredient_counts = ingredients.value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    ingredient_counts.plot(kind="bar", title="Top 10 Ingredients", color='skyblue', edgecolor='black')
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better visibility
    plt.ylabel("Frequency")
    plt.xlabel("Ingredients")
    plt.tight_layout()  # Adjust layout to prevent cutoff
    plt.show()
    plt.show()

    # Cooking Time Distribution
    plt.figure(figsize=(8, 5))  # Adjust figure size for better display
    df['time'].plot(kind='hist', bins=10, title="Cooking Time Distribution", color='lightgreen', edgecolor='black')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Frequency")
    plt.tight_layout()  # Adjust layout to prevent cutoff
    plt.show()
