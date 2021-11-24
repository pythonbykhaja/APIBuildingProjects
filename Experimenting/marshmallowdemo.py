from marshmallow import Schema, fields, schema
from pprint import pprint

class Course:
    """
    Object that needs to serialized or deserialized
    """
    def __init__(self, name, faculty,website,email) -> None:
        self.name = name
        self.faculty = faculty
        self.website = website
        self.email = email

class CourseSchema(Schema):
    """
    Schema for validating Course
    """
    name = fields.Str()
    faculty = fields.Str()
    website = fields.Url()
    email = fields.Email()


if __name__ == '__main__':
    python_course = Course(
        name='Full Stack Python', 
        faculty='Khaja', 
        website='https://python.direct',
        email='qtdevops@gmail.com')
    schema = CourseSchema()
    result = schema.dump(python_course)
    pprint(result)

