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
        :return: all the recipes
        """
        data = []
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)
        return {'data': data}, HTTPStatus.OK

    def post(self):
        """
        This method will indicate the post verb
        :return: recipe data
        """
        data = request.get_json()
        recipe = Recipe(name=data['name'],
                        description=data['description'],
                        num_of_servings=data['num_of_servings'],
                        cook_time=data['cook_time'],
                        directions=data['directions'])
        recipe_list.append(recipe)
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):
    """
    This class implements the put and get specific recipe implementations
    """

    def get(self, recipe_id):
        """
        This method implements the get request on the specific id
        :param recipe_id: recipe id to be returned
        :return: recipe if found else NOT_FOUND status
        """
        recipe = self.find_recipe(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    def put(self, recipe_id):
        """
        This method will implement the PUT request
        :param recipe_id: recipe_id to be updated
        :return: Updated Recipe data if recipe found else NOT_FOUND status
        """
        recipe = self.find_recipe(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        data = request.get_json()
        recipe.name = data['name']
        recipe.directions = data['directions']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.description = data['description']
        return recipe.data, HTTPStatus.OK

    @staticmethod
    def find_recipe(recipe_id) -> Recipe:
        """
        This method finds the recipe with the id provide
        :param recipe_id: id of the recipe
        :return: recipe if found None Otherwise
        """
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        return recipe
