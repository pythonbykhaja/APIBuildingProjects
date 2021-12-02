from flask_restful import Resource
from flask import request
from models.recipe import User
from schemas.user import UserSchema
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

user_schema = UserSchema()


class UserListRecipe(Resource):
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
