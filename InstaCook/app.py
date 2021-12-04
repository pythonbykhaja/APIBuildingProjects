from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource
from resources.user import UserListRecipe, UserResource, MeResource
from resources.token import TokenResource, RefreshResource
from config import Config
from extensions import db, jwt
from flask_migrate import Migrate


def create_app() -> Flask:
    """
    Create the Flask Application Object
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    """
    Perform database initialization and migrate the database to create tables
    :param app: flask application object
    :return: Nothing
    """
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    """
    This method registers api resources
    :param app: flask application object
    :return: Nothing
    """
    api = Api(app)

    api.add_resource(UserListRecipe, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')

    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port='5000', host='0.0.0.0', debug=True)
