from os import getenv


class Config:
    DB_USER = getenv('DB_USER', 'postgres')
    DB_PASSWORD = getenv('DB_PASSWORD', 'postgres')
    DB_HOST = getenv('DB_HOST', 'localhost')
    DB_PORT = getenv('DB_PORT', '5432')
    DB_NAME = getenv('DB_NAME', 'telegram_bot_db')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY")

    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
