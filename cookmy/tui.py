from prompt_toolkit import Application, print_formatted_text, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import ScrollOffsets
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.shortcuts import (
    message_dialog,
    input_dialog,
    yes_no_dialog,
    button_dialog,
)
from prompt_toolkit.formatted_text import ANSI, to_formatted_text, to_plain_text
from cookmy.api import (
    search_recipes_by_ingredients,
    API_ERROR,
)
from cookmy.models import convert_results_to_recipes
from cookmy.utils import format_recipes
from cookmy.tables import create_checkbox_table, create_recipe_table

# Set up the input and output fields
input_buffer = Buffer()
ingredients_buffer = Buffer()
output_field = TextArea(
    style="class:output",
    scrollbar=True,
    wrap_lines=False,
    focusable=False,
    focus_on_click=False,
)

# Set up the window layout
# Input on the left with a top pane for entering search ingredients,
# and a bottom pane for showing the ingredients entered so far for this search
# Recipe results on the right
input_window = Window(BufferControl(buffer=input_buffer), height=2, width=20)
ingredients_window = Window(BufferControl(buffer=ingredients_buffer), width=20)

input_pane = HSplit(
    [input_window, Window(height=1, char="-", style="class:line"), ingredients_window]
)

# Output window on the right, with scroll offsets
# output_window = Window(
#     BufferControl(buffer=output_buffer),
#     wrap_lines=True,
#     scroll_offsets=ScrollOffsets(top=3, bottom=3),
# )
window_separator = Window(width=1, char="|", style="class:line")

body = VSplit(
    [input_pane, window_separator, output_field],
)

help_text = "Press ENTER to add ingredient, CTRL-Z to remove last added ingredient, CTRL-F to search, CTRL-C/CTRL-Q to exit."
status_buffer = Buffer()
status_buffer.text = "Ready"


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
        # A single line for help text, with two fields for help and status message
        Window(height=1, char="-", style="class:line"),
        VSplit(
            [
                TextArea(
                    text=help_text,
                    height=1,
                    style="class:help",
                    focusable=False,
                    focus_on_click=False,
                ),
                Window(
                    BufferControl(buffer=status_buffer),
                    width=30,
                    height=1,
                    align=WindowAlign.RIGHT,
                    style="class:status",
                    dont_extend_width=True,
                ),
            ]
        ),
    ]
)

# Set up key bindings
kb = KeyBindings()


# CTRL-C to exit
@kb.add("c-c")
@kb.add("c-q")
def _(event):
    event.app.exit()


# ENTER to add ingredients to the list
@kb.add("enter")
def _(event):
    added_ingredient = input_buffer.text
    ingredients_buffer.insert_text(added_ingredient + "\n")
    input_buffer.reset()


# CTRL-Z to undo last ingredient added
@kb.add("c-z")
def _(event):
    current_ingredients = ingredients_buffer.text.split("\n")
    if len(current_ingredients) > 1:
        # Remove the last ingredient (the last element is an empty string due to the trailing newline)
        updated_ingredients = "\n".join(current_ingredients[:-2]) + "\n"
        ingredients_buffer.text = updated_ingredients
    else:
        ingredients_buffer.text = ""


# CTRL-F to run a recipe search
@kb.add("c-f")
def _(event):
    user_input = ingredients_buffer.text.split("\n")
    output_field.text = f"Searching recipes for: {user_input}"

    try:
        response = search_recipes_by_ingredients(user_input, number=5)
    except API_ERROR as e:
        output_field.text = f"API Error: {str(e)}"
        status_buffer.text = "API Error"
        return

    # TODO Check if we exceeded the quota and if we did show an error message
    quota_usage = response.get_quota_usage()
    status_buffer.text = f" | {quota_usage}"

    recipes = convert_results_to_recipes(response.content)
    for recipe in recipes:
        recipe.get_full_information()
        recipe.get_nutrition_information()
    formatted_results = format_recipes(recipes)

    recipe_table = create_recipe_table(recipes)

    formatted_table = to_plain_text(to_formatted_text(ANSI(recipe_table)))

    output_field.text = formatted_table

    selection_dialog = create_checkbox_table(formatted_table)
    selection_dialog.run()


# Put the components into an application instance
app = Application(
    layout=Layout(root_container, focused_element=input_window),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True,
)

if __name__ == "__main__":
    app.run()
