import os

class Config:
  JWT_SECRET = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  DB_HOST = os.environ.get('DB_HOST') or 'localhost'
  DB_USER = os.environ.get('DB_USER') or 'root'
  DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'docker'
  DB_DATABASE = os.environ.get('DB_DATABASE') or 'serasa-bet'
  DB_PORT = os.environ.get('DB_PORT') or '3306'

config = Config()
