import os
import datetime


class Config:
    """
    This class represents the db configuration
    """
    __username = os.getenv('DB_USER', 'sqlalchemy')
    __password = os.getenv('DB_PASSWORD', 'sqlalchemy')
    __host = os.getenv('DB_HOST', 'localhost')
    __port = os.getenv('DB_PORT', '5432')
    __db_name = os.getenv('DB_NAME', 'instacook')
    __mailgun_domain = os.getenv('MAILGUN_DOMAIN')
    __mailgun_api_key = os.getenv('MAILGUN_API_KEY')

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{__username}:{__password}@{__host}:{__port}/{__db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '11b05b0a-66ee-4448-be4d-f8f83a27ef73'
    JWT_ERROR_MESSAGE_KEY = 'message'
    MAILGUN_DOMAIN = __mailgun_domain
    MAILGUN_API_KEY = __mailgun_api_key

    # Can change when the tokens expire
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
