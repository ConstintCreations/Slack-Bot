from slack_bolt import App
from .buy_upgrade_action import buy_upgrade_action

def register(app: App):
    app.action("buy_upgrade")(buy_upgrade_action)