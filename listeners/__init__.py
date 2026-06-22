from listeners import commands, actions, events


def register_listeners(app):
    commands.register(app)
    actions.register(app)
    events.register(app)