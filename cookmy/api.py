import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("SPOONACULAR_API_KEY")

if not api_key:
    raise ValueError("SPOONACULAR_API_KEY not found in environment variables.")


def search_recipes_by_ingredients(ingredients: list, number: int = 5) -> list:
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {"ingredients": ",".join(ingredients), "apiKey": api_key, "number": number}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_recipe_information_by_id(recipe_id: int) -> dict:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key,
        "includeNutrition": True,
        "addWinePairing": True,
        "addTasteData": True,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
