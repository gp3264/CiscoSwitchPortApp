
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AD_SERVER = 'ldap://your_ad_server'
    AD_DOMAIN = 'your_domain'
    LANSWEEPER_SERVER = r'(localdb)\.\LSInstance'
    LANSWEEPER_DATABASE = 'lansweeperdb'
    LANSWEEPER_USERNAME = os.environ.get('LANSWEEPER_USERNAME') or 'your_username'
    LANSWEEPER_PASSWORD = os.environ.get('LANSWEEPER_PASSWORD') or 'your_password'
