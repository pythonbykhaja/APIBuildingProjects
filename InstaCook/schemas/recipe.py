from marshmallow import Schema, fields, validate,validates, ValidationError


def validate_num_of_servings(n):
    """
    This Method will Return Validation error if the number is less than 1
    and greater than 50
    :param n: number of servings
    :return: Validation error if number is not in the Range of 1 to 50
    """
    if n < 1:
        raise ValidationError('Number of servings must be greater than 0.')
    if n > 50:
        raise ValidationError('Number of servings must not be greater than 50. ')


class RecipeSchema(Schema):
    """
    This represents the Recipe Schema used for validation using Marshmallow
    """

    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=256)])
    num_of_servings = fields.Integer(validate=validate_num_of_servings)
    cook_time = fields.Integer()
    directions = fields.String(validate=[validate.Length(max=1000)])
    is_publish = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('cook_time')
    def validate_cook_time(self, value):
        """
        This method validates the cook time
        :param value: value of the Cook time
        :return: Validation Errors if validation fails
        """
        if value < 1:
            return ValidationError('Cook time must be greater than 0. ')
        if value > 300:
            return ValidationError('Cook time cannot be greater than 300. ')
