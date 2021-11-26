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

    @property
    def data(self):
        """
        property to return the Recipe as dictionary
        :return: dictionary representation of current Recipe object
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'num_of_servings': self.num_of_servings,
            'cook_time': self.cook_time,
            'directions': self.directions,
        }

    def save(self):
        """
        This method will be used to save the data to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        This is object based delete
        TODO: Need to implement soft_delete
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_published(cls) -> list:
        """
        This method is used to get all the published recipes
        :return: all the published recipes
        """
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        This method returns the recipe by the id
        :param recipe_id id of the recipe
        :return: returns recipe if found
        """
        return cls.query.filter_by(id=recipe_id).first()


