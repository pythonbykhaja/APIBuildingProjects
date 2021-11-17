from cmath import rect

from flask import Flask, request, jsonify
from models import recipes
from http import HTTPStatus

app = Flask(__name__)


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    """
    This method will return all the recipes
    :return: Json data with all the recipes
    """
    return jsonify(data=recipes)


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    This method will return the recipe if the id is found
    else returns NOT FOUND
    :param recipe_id: id of the recipe
    :return: recipe if found else NOT_FOUND status
    """
    recipe_found = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if recipe_found:
        return jsonify(recipe_found)
    return jsonify(message='recipe not found'), HTTPStatus.NOT_FOUND


@app.route('/recipes', methods=['POST'])
def create_recipe():
    """
    This method will create the recipe
    :return: Created Status
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """
    This method will update the recipe if found
    :param recipe_id: id of the recipe
    :return: Success when recipe is found, NOT_FOUND when id is wrong
    """
    recipe_found = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe_found:
        return jsonify(message='recipe not found'), HTTPStatus.NOT_FOUND

    data = request.get_json()
    recipe_found.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )
    return jsonify(recipe_found)


@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """
    This method will delete the recipe

    :param recipe_id: id of the recipe deleted
    :return: NOT_FOUND if recipe is not Found and Success with Status NO_CONTENT
    """
    recipe_found = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe_found:
        return jsonify(message='recipe not found'), HTTPStatus.NOT_FOUND

    recipes.remove(recipe_found)
    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
