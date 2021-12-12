from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from extensions import cache


def hash_password(password):
    """
    This method returns sha256 hash of the password entered
    :param password: password in plain text
    :return: sha-256 hash of the password
    """
    return pbkdf2_sha256.hash(password)


def check_password(password, hashed):
    """
    This method will return true if the password hashes match
    :param password: password
    :param hashed: hashed password from database
    :return: True if the match False otherwise
    """
    return pbkdf2_sha256.verify(password, hashed)


def generate_token(email, salt=None):
    """
    This method will generate a token
    :param email: email
    :param salt: sal
    :return: token
    """
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=salt)


def verify_token(token, max_age=(30 * 60), salt=None):
    """
    This method will verify the token
    :param token:
    :param max_age:
    :param salt:
    :return: Email if the verification is success else None
    """
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return None

    return email


def clear_cache(key_prefix):
    """
    Clear the cache with key_prefix
    :param key_prefix: prefix of the key
    :return: None
    """
    keys = [key for key in cache.cache._cache.keys() if key.startswith(key_prefix)]
    cache.delete_many(*keys)
