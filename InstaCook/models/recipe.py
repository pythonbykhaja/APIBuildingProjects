from passlib.handlers.oracle import oracle10

from extensions import db
from sqlalchemy import asc, desc, or_


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
            'user_id': self.user_id,
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
    def get_all_published(cls, query, page, per_page, sort, order) -> list:
        """
        This method is used to get all the published recipes
        :param query: query for the database
        :param page: page number
        :param per_page: how many records per page
        :param sort: sort by the field
        :param order: order of the sort
        :return: all the published recipes
        """

        if order == 'asc':
            sort_logic = asc(getattr(cls, sort))
        else:
            sort_logic = desc(getattr(cls, sort))

        keyword = f'%{query}%'
        return cls.query.filter(or_(cls.name.ilike(keyword),
                                    cls.description.ilike(keyword)),
                                cls.is_publish.is_(True),
                                cls.is_deleted.is_(False)). \
            order_by(sort_logic).paginate(page=page, per_page=per_page)

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        This method returns the recipe by the id
        :param recipe_id id of the recipe
        :return: returns recipe if found
        """
        return cls.query.filter_by(id=recipe_id, is_deleted=False).first()

    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        """
        This method will get all the recipes by the user
        :param user_id: id of the user
        :param visibility:
            all => get all published and unpublished recipes
            public => get all published recipes
            private => get all unpublished recipes
            deleted => get all deleted recipes
        :return: all the recipes
        """
        if visibility == 'public':
            return cls.query.filter_by(
                user_id=user_id, is_publish=True, is_deleted=False)
        elif visibility == 'private':
            return cls.query.filter_by(
                user_id=user_id, is_publish=False, is_deleted=False)
        elif visibility == 'all':
            return cls.query.filter_by(user_id=user_id, is_deleted=False)
        elif visibility == 'deleted':
            return cls.query.filter_by(user_id=user_id, is_deleted=True)
        else:
            return None


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
    is_active = db.Column(db.Boolean(), default=False, server_default="False", nullable=False)

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
        return cls.query.filter_by(username=username, is_deleted=False, is_active=True).first()

    @classmethod
    def get_by_email(cls, email, get_only_active_user=True):
        """
        Gets the user by email id
        :param email: email id
        :param get_only_active_user: to return only active users or all
        :return: user model Object
        """
        return cls.query.filter_by(email=email, is_deleted=False, is_active=get_only_active_user).first()

    @classmethod
    def get_by_id(cls, user_id):
        """
        Gets the User by the id
        :param user_id: id of the user
        :return: User model Object
        """
        return cls.query.filter_by(id=user_id, is_deleted=False, is_active=True).first()

    @property
    def data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class TokenBlackList(db.Model):
    """
    This class represents the Token Black List
    """
    __tablename__ = 'tokenblacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        """
        This method will be used to save the data to the database
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_jti(cls, jti):
        """
        This method will search for the token in the black list model
        :param jti: jti of the jwt toke
        :return: token if found, None if not found
        """
        return cls.query.filter_by(jti=jti).first()
