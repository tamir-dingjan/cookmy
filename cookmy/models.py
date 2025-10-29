from cookmy.api import get_recipe_information_by_id, get_recipe_nutrition_by_id


class Recipe:
    def __init__(self, content: dict):
        self.id = content.get("id", "")
        self.title = content.get("title", "").title()
        self.usedIngredientCount = content.get("usedIngredientCount", 0)
        self.missedIngredientCount = content.get("missedIngredientCount", 0)
        self.usedIngredients = content.get("usedIngredients", [])
        self.missedIngredients = content.get("missedIngredients", [])

    def __repr__(self):
        return f"<Recipe {self.title}>"

    def get_full_information(self):
        self.data = get_recipe_information_by_id(self.id)
        self.source = self.data.content.get("sourceName", "")
        self.timings = {
            "ready": self.data.content.get("readyInMinutes", 0),
            "cooking": self.data.content.get("cookingTime", 0),
            "prep": self.data.content.get("prepTime", 0),
        }
        self.pairings = {
            "wines": self.data.content.get("winePairing", {}).get("pairedWines", []),
            "text": self.data.content.get("winePairing", {}).get("pairingText", ""),
        }

    def get_nutrition_information(self):
        self.nutrition_data = get_recipe_nutrition_by_id(self.id)
        self.nutrition = self.nutrition_data.content


def convert_results_to_recipes(results: list) -> list:
    recipes = [Recipe(item) for item in results]
    return recipes
