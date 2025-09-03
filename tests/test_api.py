from cookmy.api import api_key, search_recipes_by_ingredients


def test_api_key():
    assert api_key is not None
    assert len(api_key) > 0


def test_search_recipes_by_ingredients():
    ingredients = ["chicken", "rice"]
    recipes = search_recipes_by_ingredients(ingredients, number=3)
    assert isinstance(recipes, list)
    assert len(recipes) <= 3
    for recipe in recipes:
        assert "id" in recipe
        assert "title" in recipe
        assert "image" in recipe
