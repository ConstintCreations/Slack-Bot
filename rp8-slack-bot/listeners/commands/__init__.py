from slack_bolt import App
from .cast_command import cast_command


def register(app: App):
    app.command("/cast")(cast_command)