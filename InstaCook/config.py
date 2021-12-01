import os


class Config:
    """
    This class represents the db configuration
    """
    __username = os.getenv('DB_USER', 'sqlalchemy')
    __password = os.getenv('DB_PASSWORD', 'sqlalchemy')
    __host = os.getenv('DB_HOST', 'localhost')
    __port = os.getenv('DB_PORT', '5432')
    __db_name = os.getenv('DB_NAME', 'instacook')

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{__username}:{__password}@{__host}:{__port}/{__db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '11b05b0a-66ee-4448-be4d-f8f83a27ef73'
    JWT_ERROR_MESSAGE_KEY = 'message'
