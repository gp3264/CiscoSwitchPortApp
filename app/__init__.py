from app.cli_commands import CLICommands
from app.cli_connection import CLIConnection

from flask import Flask
from .config import Config
from .database import Database
from .routes import main
from .models import MdtaRegion

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        Database.init_app(self.app)

    def create_app(self):
        with self.app.app_context():
            Database.create_all(self.app)
            self.populate_regions()
        self.app.register_blueprint(main)
        return self.app

    def populate_regions(self):
        regions = ['Central', 'North', 'South']
        for region_name in regions:
            if not MdtaRegion.query.filter_by(region_name=region_name).first():
                region = MdtaRegion(region_name=region_name)
                Database.db.session.add(region)
        Database.db.session.commit()
