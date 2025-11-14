import os
from dotenv import load_dotenv
import requests


class API_ERROR(Exception):
    pass


class api_response:
    def __init__(self, response):
        self.raw_response = response
        self.status_code = response.status_code
        self.content = response.json()
        self.quota_used = response.headers.get("X-API-Quota-Used")
        self.quota_left = response.headers.get("X-API-Quota-Left")

    def get_quota_usage(self) -> str:
        quota_used = float(self.quota_used)
        quota_left = float(self.quota_left)
        pc_used = quota_used / (quota_used + quota_left) * 100
        return f"% quota used: {pc_used:.1f}"


load_dotenv()
api_key = os.getenv("SPOONACULAR_API_KEY")

if not api_key:
    print("Have you configured your API key in your enrivonment?")
    raise ValueError("SPOONACULAR_API_KEY not found in environment variables.")

def search_recipes_by_ingredients(ingredients: list, number: int = 5) -> api_response:
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {"ingredients": ",".join(ingredients), "apiKey": api_key, "number": number}
    response = api_response(requests.get(url, params=params))
    if response.status_code == 200:
        return response
    else:
        raise API_ERROR(
            f"API request failed with status code {response.status_code} and the following error message:\n {response.content.get('message', 'No error message provided')}"
        )


def get_recipe_information_by_id(recipe_id: int) -> api_response:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key,
        "includeNutrition": True,
        "addWinePairing": True,
        "addTasteData": True,
    }
    response = api_response(requests.get(url, params=params))
    if response.status_code == 200:
        return response
    else:
        raise API_ERROR(
            f"API request failed with status code {response.status_code} and the following error message:\n {response.content.get('message', 'No error message provided')}"
        )


def get_recipe_nutrition_by_id(recipe_id: int) -> api_response:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": api_key}
    response = api_response(requests.get(url, params=params))
    if response.status_code == 200:
        return response
    else:
        raise API_ERROR(
            f"API request failed with status code {response.status_code} and the following error message:\n {response.content.get('message', 'No error message provided')}"
        )
