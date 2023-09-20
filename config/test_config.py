# test config for app
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///music_app_test"
    SECRET_KEY = "SHHHHHH"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
