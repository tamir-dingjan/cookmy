from cookmy.cli import parse_args
from cookmy.api import search_recipes_by_ingredients
from cookmy.models import convert_results_to_recipes
from cookmy.utils import format_recipes

if __name__ == "__main__":
    args = parse_args()
    results = search_recipes_by_ingredients(args.ingredients, args.number)
    recipes = convert_results_to_recipes(results.content)
    for recipe in recipes:
        recipe.get_full_information()
        recipe.get_nutrition_information()
    formatted_results = format_recipes(recipes)
    print(formatted_results)
