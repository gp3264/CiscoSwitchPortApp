# from app.cli_commands import CLICommands
# from app.cli_connection import CLIConnection
from app.cli_commands_templates import CLIExecutive
from app import *
from app.cli_commands_templates import *
from app.application_dataclasses_support import *
from app.cli_commands import *
from app.cli_commands_templates import *
from app.cli_connection import *
from app.application_dataclass_data_manager import *







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


