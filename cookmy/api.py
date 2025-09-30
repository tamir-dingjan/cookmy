import os
from dotenv import load_dotenv
import requests


class API_ERROR(Exception):
    pass


load_dotenv()
api_key = os.getenv("SPOONACULAR_API_KEY")

if not api_key:
    raise ValueError("SPOONACULAR_API_KEY not found in environment variables.")


def get_quota_usage_from_response(response) -> str:
    quota_used = response.headers.get("X-API-Quota-Used")
    quota_left = response.headers.get("X-API-Quota-Left")
    pc_used = quota_used / (quota_used + quota_left) * 100
    return f"% quota used: {pc_used:.2f}"


def search_recipes_by_ingredients(ingredients: list, number: int = 5) -> list:
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {"ingredients": ",".join(ingredients), "apiKey": api_key, "number": number}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise API_ERROR(
            f"API request failed with status code {response.status_code} and the following error message:\n {response.json().get('message', 'No error message provided')}"
        )


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


def get_recipe_nutrition_by_id(recipe_id: int) -> dict:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
