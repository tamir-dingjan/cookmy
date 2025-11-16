class AppState:
    def __init__(self):
        self.mode = "search"
        self.saved_recipes = ["No saved recipes"]

    def view_saved_recipes(self) -> str:
        return "\n".join(self.saved_recipes)
