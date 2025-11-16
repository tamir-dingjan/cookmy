from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from views.search_view import create_search_view
from views.saved_view import create_saved_view


def create_keybindings(state):
    kb = KeyBindings()

    @kb.add("1")
    def _(event):
        state.mode = "search"
        event.app.layout = Layout(create_search_view(state))

    @kb.add("2")
    def _(event):
        state.mode = "saved"
        event.app.layout = Layout(create_saved_view(state))

    @kb.add("c-c")
    @kb.add("q")
    def _(event):
        event.app.exit()

    return kb
