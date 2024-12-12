from database import create_database
import recipe_manager
import analysis


def main_menu():
    while True:
        print("\nWelcome to Recipe Manager")
        print("1. Add a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. View data analysis & visualizations")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            recipe_manager.add_recipe_ui()
        elif choice == '2':
            recipe_manager.search_recipe_ui()
        elif choice == '3':
            recipe_manager.update_recipe_ui()
        elif choice == '4':
            recipe_manager.delete_recipe_ui()
        elif choice == '5':
            analysis.analyze_recipes()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_database()
    main_menu()
