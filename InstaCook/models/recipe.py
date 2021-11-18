recipe_list = []


def get_last_id():
    """
    This method will return the recipe id
    """
    if recipe_list:
        last_recipe = recipe_list[-1]
    else:
        return 1
    return last_recipe.id + 1


class Recipe:
    """
    This class represents the Recipe Model
    """

    def __init__(self, name, description, num_of_servings, cook_time, directions):
        """
        The initializer for the recipe
        :param name: name of the recipe
        :param description: description
        :param num_of_servings: number of servings
        :param cook_time: cook_time in seconds
        :param directions: directions to follow
        """
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.num_of_servings = num_of_servings
        self.cook_time = cook_time
        self.directions = directions
        self.is_publish = False

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

