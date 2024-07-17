from app.cli_commands import CLICommands
from app.cli_connection import CLIConnection

from flask import Flask
from .config import Config
from .database import Database
from .routes import main


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        Database.init_app(self.app)

    def create_app(self):
        self.app.register_blueprint(main)
        return self.app


