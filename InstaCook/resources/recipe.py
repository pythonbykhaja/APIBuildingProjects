from cmath import rect
from http import HTTPStatus

from flask import request
from flask_restful import Resource

from models.recipe import Recipe
from schemas.recipe import RecipeSchema, RecipePaginationSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from webargs import fields
from webargs.flaskparser import use_kwargs

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)
recipe_pagination_schema = RecipePaginationSchema()


class RecipeListResource(Resource):
    """
    The Resource that will be exposing the Recipe List
    """

    @use_kwargs({'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=2),
                 'q': fields.Str(missing='')})
    def get(self, page, per_page, q):
        """
        This method will indicate the get verb
        :return: all the recipes
        """
        # todo: need to fix kwargs workaround
        page = int(request.args.get('page', default="1"))
        per_page = int(request.args.get('per_page', default="2"))
        query = request.args.get('q', default='')
        paginated_recipes = Recipe.get_all_published(
            page=page, per_page=per_page, query=query
        )
        return recipe_pagination_schema.dump(paginated_recipes), HTTPStatus.OK

    @jwt_required()
    def post(self):
        """
        This method will indicate the post verb
        :return: recipe data
        """
        json_data = request.get_json()

        errors = recipe_schema.validate(data=json_data)
        if errors:
            return {'message': 'Validation Error', 'error': errors}, HTTPStatus.BAD_REQUEST
        current_user = get_jwt_identity()
        data = recipe_schema.load(data=json_data)
        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):
    """
    This class implements the put and get specific recipe implementations
    """

    @jwt_required(optional=True)
    def get(self, recipe_id):
        """
        This method implements the get request on the specific id
        :param recipe_id: recipe id to be returned
        :return: recipe if found else NOT_FOUND status
        """
        recipe = Recipe.get_by_id(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if recipe.is_publish is False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe.data, HTTPStatus.OK

    @jwt_required()
    def put(self, recipe_id):
        """
        This method will implement the PUT request
        :param recipe_id: recipe_id to be updated
        :return: Updated Recipe data if recipe found else NOT_FOUND status
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

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

    @jwt_required()
    def patch(self, recipe_id):
        """
        This method will implement the partial update of the recipe
        The only mandatory body item will be name i.e name of the recipe
        :return: status ok if the update is successful,
            status BAD Request if the validation fails
            Status un authorized if the user has no authorization
            Status Forbidden if the user is not allowed to perform the operation
        """
        json_data = request.get_json()

        errors = recipe_schema.validate(data=json_data, partial=('name',))
        if errors:
            return {'message': 'Validation Error', 'error': errors}, HTTPStatus.BAD_REQUEST
        data = recipe_schema.load(data=json_data, partial=('name',))

        # get recipe from model
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message', 'Access is denied'}, HTTPStatus.FORBIDDEN

        # defensive mechanism to update the items if the are present in payload
        recipe.name = data.get('name') or recipe.name
        recipe.directions = data.get('directions') or recipe.directions
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.description = data.get('description') or recipe.description
        # saving the recipe to the model
        recipe.save()

        # serializing the schema
        return recipe_schema.dump(recipe), HTTPStatus.OK

    @jwt_required()
    def delete(self, recipe_id):
        """
        Delete implementation of the Recipe

        :param recipe_id: id of the recipe to be deleted
        :return: NO_CONTENT if the Recipe is deleted and NOT_FOUND if the recipe is not found
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.delete()
        return {}, HTTPStatus.NO_CONTENT


class RecipePublishResource(Resource):
    """
    This class represents a Rest Resource to Publish and UnPublish Recipes
    """

    @jwt_required()
    def put(self, recipe_id):
        """
        This method is used to publish the Recipe
        :param recipe_id: id of the recipe
        :return: SUCCESS if recipe is found and NOT_FOUND status otherwise
        """
        recipe = Recipe.get_by_id(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT

    @jwt_required()
    def delete(self, recipe_id):
        """
        This method will un publish the Recipe
        :param recipe_id: id of the Recipe
        :return: SUCCESS when recipe is unpublished and NOT_FOUND if the recipe is not found
        """
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = False
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT
