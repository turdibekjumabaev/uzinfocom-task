import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv('DEBUG', False)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    ESKIZ_EMAIL = os.getenv('ESKIZ_EMAIL', None)
    ESKIZ_PASSWORD = os.getenv('ESKIZ_PASSWORD', None)
