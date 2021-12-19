from flask import Flask, request
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
from extensions import db, jwt, cache, limiter, docs
from flask_migrate import Migrate
from models.recipe import TokenBlackList


def create_app() -> Flask:
    """
    Create the Flask Application Object
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    api_spec = app.config.get('APISPEC_SPEC')
    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    api_spec.components.security_scheme("jwt", jwt_scheme)
    app.config.update(APISPEC_SPEC=api_spec)
    register_extensions(app)
    register_resources(app, docs)
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
    docs.init_app(app)


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

    @limiter.request_filter
    def ip_whitelist():
        return request.remote_addr == "127.0.0.1"

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


def register_resources(app, docs):
    """
    This method registers api resources
    :param app: flask application object
    :param docs: Swagger documentation
    :return: Nothing
    """

    api = Api(app)

    api.add_resource(UserListResource, '/users')
    docs.register(UserListResource)
    api.add_resource(UserResource, '/users/<string:username>')
    docs.register(UserResource)
    api.add_resource(MeResource, '/me')
    docs.register(MeResource)
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    docs.register(UserRecipeListResource)
    api.add_resource(UserActivationResource, '/users/activate/<string:token>')
    docs.register(UserActivationResource)

    api.add_resource(TokenResource, '/token')
    docs.register(TokenResource)
    api.add_resource(RefreshResource, '/refresh')
    docs.register(RefreshResource)
    api.add_resource(RevokeResource, '/revoke')
    docs.register(RevokeResource)

    api.add_resource(RecipeListResource, '/recipes')
    docs.register(RecipeListResource)
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    docs.register(RecipeResource)
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    docs.register(RecipePublishResource)


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port=5000, host='0.0.0.0', debug=True)
