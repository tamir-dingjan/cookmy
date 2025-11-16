from prompt_toolkit.layout import HSplit
from prompt_toolkit.widgets import TextArea, Label


def create_saved_view(state):
    print(state.saved_recipes)
    saved_text = TextArea(text=state.view_saved_recipes(), read_only=True)
    return HSplit(
        [
            Label(text="Saved recipes"),
            saved_text,
        ]
    )
