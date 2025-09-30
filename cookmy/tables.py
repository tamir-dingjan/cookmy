# tables for displaying recipes in the TUI
from io import StringIO
from rich.console import Console
from rich.table import Table


def create_recipe_table(recipes) -> str:
    table = Table(title="Recipe Results")

    table.add_column("Title", width=20)
    table.add_column("Extra Ingredients", width=20)
    table.add_column("Ready In (min)", justify="right", width=15)
    table.add_column("Calories", justify="right", width=10)
    table.add_column("Carbs", justify="right", width=7)
    table.add_column("Fat", justify="right", width=7)
    table.add_column("Protein", justify="right", width=7)

    for recipe in recipes:
        calories = (
            recipe.nutrition.get("calories", "N/A") if recipe.nutrition else "N/A"
        )
        carbs = recipe.nutrition.get("carbs", "N/A") if recipe.nutrition else "N/A"
        fat = recipe.nutrition.get("fat", "N/A") if recipe.nutrition else "N/A"
        protein = recipe.nutrition.get("protein", "N/A") if recipe.nutrition else "N/A"

        table.add_row(
            recipe.title,
            str(recipe.missedIngredientCount),
            str(recipe.timings.get("ready", "N/A")),
            str(calories),
            str(carbs),
            str(fat),
            str(protein),
        )

    console = Console()
    with console.capture() as capture:
        console.print(table)
    # Return the table as a string for display in the TUI
    table_str = capture.get()
    return table_str
