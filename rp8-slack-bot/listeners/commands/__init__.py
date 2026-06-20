from slack_bolt import App
from .cast_command import cast_command
from .reel_command import reel_command


def register(app: App):
    app.command("/cast")(cast_command)
    app.command("/reel")(reel_command)