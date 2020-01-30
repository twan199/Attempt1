class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass
