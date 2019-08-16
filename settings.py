import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data.db')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
