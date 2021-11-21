from extensions import db

recipe_list = []


def get_last_id():
    """
    This method will return the last id
    :return: id to be generated
    """
    if recipe_list:
        last_recipe = recipe_list[-1]
    else:
        return 1

    return last_recipe.id + 1


class Recipe(db.Model):
    """
    This class represents the Recipe Model
    """
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(256))
    num_of_servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    directions = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

