from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()
