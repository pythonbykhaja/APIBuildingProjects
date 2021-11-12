from flask import Flask, request, jsonify
from models import recipes

app = Flask(__name__)


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    """
    This method will return all the recipes
    :return: Json data with all the recipes
    """
    return jsonify(data=recipes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
