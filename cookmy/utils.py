def format_recipes(recipes: list) -> str:
    if not recipes:
        return "No recipes found."

    formatted = []
    for recipe in recipes:
        formatted.append("/" + "-" * (len(recipe.title) + 2) + "\\")
        formatted.append(f"| {recipe.title} |")
        formatted.append("\\" + "-" * (len(recipe.title) + 2) + "/")

        if recipe.source:
            formatted.append(f"By: {recipe.source}")

        if recipe.usedIngredientCount != 0:
            used_ingredients = ", ".join(
                [ingredient["name"] for ingredient in recipe.usedIngredients]
            )
            formatted.append(
                f"Uses your ingredients ({recipe.usedIngredientCount}): {used_ingredients}"
            )

        if recipe.missedIngredientCount != 0:
            missed_ingredients = ", ".join(
                [ingredient["name"] for ingredient in recipe.missedIngredients]
            )
            formatted.append(
                f"Additional required ingredients ({recipe.missedIngredientCount}): {missed_ingredients}"
            )

        if recipe.timings["ready"] != 0:
            formatted.append(f"Ready in {recipe.timings['ready']} minutes")
        if recipe.timings["prep"] != 0:
            formatted.append(f"Prep time: {recipe.timings['prep']} minutes")
        if recipe.timings["cooking"] != 0:
            formatted.append(f"Cooking time: {recipe.timings['cooking']} minutes")

        formatted.append("")

        if recipe.pairings["wines"] != []:
            formatted.append(
                f"Recommended wine pairings: {', '.join(recipe.pairings['wines'])}"
            )
        if recipe.pairings["text"] != "":
            formatted.append(f"{recipe.pairings['text']}")

        if recipe.nutrition:
            formatted.append("Nutrition Information:")
            formatted.append(f"  Calories: {recipe.nutrition.get('calories', 'N/A')}")
            formatted.append(f"  Carbs: {recipe.nutrition.get('carbs', 'N/A')}")
            formatted.append(f"  Fat: {recipe.nutrition.get('fat', 'N/A')}")
            formatted.append(f"  Protein: {recipe.nutrition.get('protein', 'N/A')}")

        formatted.append("")

    return "\n".join(formatted)
