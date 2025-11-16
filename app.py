from prompt_toolkit import Application
from prompt_toolkit.layout import Layout

from models.state import AppState
from views.saved_view import create_saved_view
from controllers.keybindings import create_keybindings


def create_application():
    state = AppState()
    root_layout = Layout(create_saved_view(state))
    kb = create_keybindings(state)

    return Application(
        layout=root_layout,
        key_bindings=kb,
        full_screen=True,
    )


def run_app():
    create_application().run()
