from slack_bolt import App
from .cast_command import cast_command
from .reel_command import reel_command
from .sell_command import sell_command
from .fishdex_command import fishdex_command
from .shop_command import shop_command

def register(app: App):
    app.command("/cast")(cast_command)
    app.command("/reel")(reel_command)
    app.command("/sell")(sell_command)
    app.command("/fishdex")(fishdex_command)
    app.command("/shop")(shop_command)