from flask_restful import Resource
from flask import request
from webargs import fields

from models.recipe import User, Recipe
from schemas.recipe import RecipeSchema
from schemas.user import UserSchema
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from webargs.flaskparser import use_kwargs

user_schema = UserSchema()
recipe_list_schema = RecipeSchema(many=True)


class UserListResource(Resource):
    """
    This class implements the User Resource
    """

    def post(self):
        """
        This represent the post call
        :return:
        """
        json_data = request.get_json()

        errors = user_schema.validate(data=json_data)
        if errors:
            return {'message': 'Validation Errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        data = user_schema.load(data=json_data)

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        return user.data, HTTPStatus.CREATED


class UserResource(Resource):
    """
    This resource will be used to get the user profile
    """

    @jwt_required(optional=True)
    def get(self, username):
        """
        This method will get the user profile information
        :param username: username of the user
        :return: username and email id
        """
        user = User.get_by_username(username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user_id = get_jwt_identity()

        if current_user_id == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        else:
            data = {
                'username': user.username
            }
        return data, HTTPStatus.OK


class MeResource(Resource):
    """
    This class will send the user information only for the logged users
    if the user is not logged 401 unauthenticated status should be sent
    """

    @jwt_required()
    def get(self):
        """
        Get the user information of the logged in user
        :return: user info
        """
        user = User.get_by_id(get_jwt_identity())
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data, HTTPStatus.OK


class UserRecipeListResource(Resource):
    """
    This resource represents the recipes of the user
    """

    @jwt_required()
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        """
        This method will return recipes of a user depending on visibility
        :param username: author of the recipes
        :param visibility: public|private|all
        :return:
        """
        user = User.get_by_username(username)

        #todo: need to fix the visibility for webargs parser

        visibility = request.args.get('visibility')

        if user is None:
            return {'message', 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private', 'deleted']:
            pass
        elif current_user != user.id and visibility in ['all', 'private', 'deleted']:
            return {'message': 'Access denied'}, HTTPStatus.FORBIDDEN
        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)
        return recipe_list_schema.dump(recipes)['data'], HTTPStatus.OK

