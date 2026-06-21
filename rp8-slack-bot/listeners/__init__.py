from listeners import commands, actions


def register_listeners(app):
    commands.register(app)
    actions.register(app)