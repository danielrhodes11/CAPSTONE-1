import os


class DevConfig:
    # Set the SQLALCHEMY_DATABASE_URI using os.environ.get() with a default value
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql:///playlistify')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = 'secret'
