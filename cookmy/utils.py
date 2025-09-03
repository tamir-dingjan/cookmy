def format_recipes(recipes: list) -> str:
    if not recipes:
        return "No recipes found."

    formatted = []
    for recipe in recipes:
        title = recipe.get("title", "No title")
        used_count = recipe.get("usedIngredientCount", 0)
        missed_count = recipe.get("missedIngredientCount", 0)
        formatted.append(
            f"Title: {title}\nUsed Ingredients: {used_count}\nMissed Ingredients: {missed_count}\n"
        )

    return "\n".join(formatted)
