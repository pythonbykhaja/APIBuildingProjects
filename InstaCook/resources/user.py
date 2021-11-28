from flask_restful import Resource
from flask import request
from models.recipe import User
from schemas.user import UserSchema
from http import HTTPStatus

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
            return {'message': 'Validation Errors', 'errors': errors }, HTTPStatus.BAD_REQUEST
        data = user_schema.load(data=json_data)

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        return user.data, HTTPStatus.CREATED
