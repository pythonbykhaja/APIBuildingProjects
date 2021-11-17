from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):
    """
    The Resource that will be exposing the Recipe List
    """

    def get(self):
        """
        This method will indicate the get verb
        :return:
        """
        pass

    def post(self):
        """
        This method will indicate the post verb
        :return:
        """
        pass
