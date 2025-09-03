from cookmy.cli import parse_args
from cookmy.api import search_recipes_by_ingredients
from cookmy.utils import format_recipes

if __name__ == "__main__":
    args = parse_args()
    results = search_recipes_by_ingredients(args.ingredients, args.number)
    formatted_results = format_recipes(results)
    print(formatted_results)
