from passlib.hash import pbkdf2_sha256


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
