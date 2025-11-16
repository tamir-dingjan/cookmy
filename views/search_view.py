from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.widgets import TextArea


def create_search_view(state):
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
        [
            input_window,
            Window(height=1, char="-", style="class:line"),
            ingredients_window,
        ]
    )

    # Output window on the right, with scroll offsets
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
    return root_container
