from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apispec import FlaskApiSpec

db: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()
cache: Cache = Cache()
limiter: Limiter = Limiter(key_func=get_remote_address)
docs: FlaskApiSpec = FlaskApiSpec()
