from http import HTTPStatus

from flask import request
from flask_restful import Resource

from models.recipe import Recipe
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)


class RecipeListResource(Resource):
    """
    The Resource that will be exposing the Recipe List
    """

    def get(self):
        """
        This method will indicate the get verb
        :return: all the recipes
        """
        recipes = Recipe.get_all_published()
        return recipe_list_schema.dump(recipes)['data'], HTTPStatus.OK

    def post(self):
        """
        This method will indicate the post verb
        :return: recipe data
        """
        json_data = request.get_json()

        errors = recipe_schema.validate(data=json_data)
        if errors:
            return {'message': 'Validation Error', 'error': errors}, HTTPStatus.BAD_REQUEST
        data = recipe_schema.load(data=json_data)
        recipe = Recipe(**data)
        recipe.save()
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
        recipe = Recipe.get_by_id(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    def put(self, recipe_id):
        """
        This method will implement the PUT request
        :param recipe_id: recipe_id to be updated
        :return: Updated Recipe data if recipe found else NOT_FOUND status
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        json_data = request.get_json()
        errors = recipe_schema.validate(data=json_data)
        if errors:
            return {'message': 'Validation Error', 'error': errors}, HTTPStatus.BAD_REQUEST

        data = recipe_schema.load(data=json_data)
        recipe.name = data['name']
        recipe.directions = data['directions']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.description = data['description']
        recipe.save()
        return recipe.data, HTTPStatus.OK

    def delete(self, recipe_id):
        """
        Delete implementation of the Recipe

        :param recipe_id: id of the recipe to be deleted
        :return: NO_CONTENT if the Recipe is deleted and NOT_FOUND if the recipe is not found
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.delete()
        return {}, HTTPStatus.NO_CONTENT


class RecipePublishResource(Resource):
    """
    This class represents a Rest Resource to Publish and UnPublish Recipes
    """

    def put(self, recipe_id):
        """
        This method is used to publish the Recipe
        :param recipe_id: id of the recipe
        :return: SUCCESS if recipe is found and NOT_FOUND status otherwise
        """
        recipe = Recipe.get_by_id(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, recipe_id):
        """
        This method will un publish the Recipe
        :param recipe_id: id of the Recipe
        :return: SUCCESS when recipe is unpublished and NOT_FOUND if the recipe is not found
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT
