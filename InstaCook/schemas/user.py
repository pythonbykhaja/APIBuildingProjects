from marshmallow import Schema, fields
from utils import hash_password

class UserSchema(Schema):
    """
    This class represents the user schema
    """
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')

    def load_password(self, value):
        """
        Returns the hash of the password
        :param value: value
        :return: hash of the password
        """
        return hash_password(value)
