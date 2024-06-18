
from flask_sqlalchemy import SQLAlchemy

class Database:
    db = SQLAlchemy()

    @staticmethod
    def init_app(app):
        Database.db.init_app(app)

    @staticmethod
    def create_all(app):
        with app.app_context():
            Database.db.create_all()
