import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    SESSION_COOKIE_SECURE = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Simplex'
    db_dir = "database/db.sqlite"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_DIR = os.path.join(BASE_DIR, '../logs')

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
