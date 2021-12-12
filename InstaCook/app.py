from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource
from resources.user import (
    UserListResource,
    UserResource,
    MeResource,
    UserRecipeListResource,
    UserActivationResource
)
from resources.token import TokenResource, RefreshResource, RevokeResource
from config import Config
from extensions import db, jwt, cache, limiter
from flask_migrate import Migrate
from models.recipe import TokenBlackList


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
    cache.init_app(app)
    limiter.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_black_list(jwt_header, jwt_payload):
        """
        This function will check for the validity of the token.
        If the user has logged out, the token appears in blocked list
        :param jwt_header:
        :param jwt_payload:
        :return:
        """
        jti = jwt_payload["jti"]
        token = TokenBlackList.get_by_jti(jti)
        return token is not None

    # Note: uncomment below code to understand the keys added to cache
    #@app.before_request
    #def before_request():
    #    print('\n==================== BEFORE REQUEST =====================')
    #    print(cache.cache._cache.keys())
    #    print('\n=========================================================')

    # @app.after_request
    # def after_request(response):
    #     print('\n====================  AFTER REQUEST =====================')
    #     print(cache.cache._cache.keys())
    #     print('\n=========================================================')
    #     return response


def register_resources(app):
    """
    This method registers api resources
    :param app: flask application object
    :return: Nothing
    """
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserActivationResource, '/users/activate/<string:token>')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port=5000, host='0.0.0.0', debug=True)
