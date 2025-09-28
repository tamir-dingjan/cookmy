from cookmy.api import get_recipe_information_by_id, get_recipe_nutrition_by_id


class Recipe:
    def __init__(self, response):
        self.id = response.get("id", "")
        self.title = response.get("title", "").title()
        self.usedIngredientCount = response.get("usedIngredientCount", 0)
        self.missedIngredientCount = response.get("missedIngredientCount", 0)
        self.usedIngredients = response.get("usedIngredients", [])
        self.missedIngredients = response.get("missedIngredients", [])

    def __repr__(self):
        return f"<Recipe {self.title}>"

    def get_full_information(self):
        self.data = get_recipe_information_by_id(self.id)
        self.source = self.data.get("sourceName", "")
        self.timings = {
            "ready": self.data.get("readyInMinutes", 0),
            "cooking": self.data.get("cookingTime", 0),
            "prep": self.data.get("prepTime", 0),
        }
        self.pairings = {
            "wines": self.data.get("winePairing", {}).get("pairedWines", []),
            "text": self.data.get("winePairing", {}).get("pairingText", ""),
        }

    def get_nutrition_information(self):
        self.nutrition = get_recipe_nutrition_by_id(self.id)


def convert_results_to_recipes(results: list) -> list:
    recipes = [Recipe(item) for item in results]
    return recipes
