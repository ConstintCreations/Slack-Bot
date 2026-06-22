from slack_bolt import App
from .home_opened_event import home_opened_event

def register(app: App):
    app.event("app_home_opened")(home_opened_event)