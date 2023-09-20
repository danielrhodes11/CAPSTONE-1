import os


class DevConfig:
    # Set the SQLALCHEMY_DATABASE_URI using os.environ.get() with a default value
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql:///music_app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = 'secret'
