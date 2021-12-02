from flask_restful import Resource
from flask import request
from http import HTTPStatus
from models.recipe import User
from utils import check_password
from flask_jwt_extended import create_access_token


class TokenResource(Resource):
    """
    This class will implement the token resource,
    where the user is expected to login and gets the access token as response
    if the user is created
    """

    def post(self):
        """
        This method represents the post call with the body containing
        email and password
        :return: access_token in the response if the user is valid
        """
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        user = User.get_by_email(email)
        if not user or not check_password(password, user.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, HTTPStatus.OK
