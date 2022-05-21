from flask import Blueprint

example_blueprint = Blueprint('testBlueprint', __name__)

@example_blueprint.route('/testBlueprint')
def index():
    return "This is an example app"