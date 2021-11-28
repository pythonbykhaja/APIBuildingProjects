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
    is_deleted = db.Column(db.Boolean(), default=False, server_default="False", nullable=False)
    # foreign key
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="recipes")

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
        We implement the soft delete pattern
        """
        self.is_deleted = True
        self.save()

    def restore(self):
        """
        restore the recipe
        """
        self.is_deleted = False
        self.save()

    @classmethod
    def get_all_published(cls) -> list:
        """
        This method is used to get all the published recipes
        :return: all the published recipes
        """
        return cls.query.filter_by(is_publish=True, is_deleted=False).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        This method returns the recipe by the id
        :param recipe_id id of the recipe
        :return: returns recipe if found
        """
        return cls.query.filter_by(id=recipe_id, is_deleted=False).first()


class User(db.Model):
    """
    This class represents the user model
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, server_default="False", nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    # relationship not a field in database
    recipes = db.relationship('Recipe', backref='user')

    def save(self):
        """
        This method will be used to save the data to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        This is object based delete
        We implement the soft delete pattern
        """
        self.is_deleted = True
        self.save()

    def restore(self):
        """
        restore the recipe
        """
        self.is_deleted = False
        self.save()

    @classmethod
    def get_by_username(cls, username):
        """
        Gets the user by the username
        :param username: username
        :return: user model object
        """
        return cls.query.filter_by(username=username, is_deleted=False).first()

    @classmethod
    def get_by_email(cls, email):
        """
        Gets the user by email id
        :param email: email id
        :return: user model Object
        """
        return cls.query.filter_by(email=email, is_deleted=False).first()

    @classmethod
    def get_by_id(cls, user_id):
        """
        Gets the User by the id
        :param user_id: id of the user
        :return: User model Object
        """
        return cls.query.filter_by(id=user_id, is_deleted=False).first()

    @property
    def data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

