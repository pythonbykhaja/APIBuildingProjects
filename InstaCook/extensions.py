from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache

db: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()
cache: Cache = Cache()
