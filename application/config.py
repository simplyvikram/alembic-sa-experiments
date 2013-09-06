
class Config(object):
    pass


class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '!!!!CHANGE ME!!!!'
    DATABASE_URI = '!!!!CHANGE ME!!!'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'secret key'
    DATABASE_URI = 'postgresql+psycopg2://devuser:devuser@localhost:5432/' \
                   'alembic-sa-experiments'


