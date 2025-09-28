from prompt_toolkit import Application, print_formatted_text, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.shortcuts import (
    message_dialog,
    input_dialog,
    yes_no_dialog,
    button_dialog,
)

from cookmy.api import search_recipes_by_ingredients
from cookmy.models import convert_results_to_recipes
from cookmy.utils import format_recipes

# Set up the input and output buffers
input_buffer = Buffer()
output_buffer = Buffer()

# Set up the window layout
# Input on the left, results on the right
input_window = Window(BufferControl(buffer=input_buffer))
output_window = Window(BufferControl(buffer=output_buffer))
window_separator = Window(width=1, char="|", style="class:line")

body = VSplit(
    [input_window, window_separator, output_window],
)

root_container = HSplit(
    [
        # A static header
        Window(
            height=1,
            content=FormattedTextControl([("class:title", "CookMy")]),
            align=WindowAlign.CENTER,
        ),
        # A horizontal separator between the head and body
        Window(height=1, char="-", style="class:line"),
        body,
    ]
)

# Set up key bindings
kb = KeyBindings()


# CTRL-C to exit
@kb.add("c-c")
def _(event):
    event.app.exit()


# ENTER to run a recipe search
@kb.add("enter")
def _(event):
    user_input = input_buffer.text
    output_buffer.text = f"Searching recipes for: {user_input}"

    results = search_recipes_by_ingredients(user_input.split(","), number=5)

    recipes = convert_results_to_recipes(results)
    for recipe in recipes:
        recipe.get_full_information()
        recipe.get_nutrition_information()
    formatted_results = format_recipes(recipes)

    output_buffer.text = formatted_results

    input_buffer.text = ""


# Put the components into an application instance
app = Application(
    layout=Layout(root_container, focused_element=input_window),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True,
)

if __name__ == "__main__":
    app.run()
