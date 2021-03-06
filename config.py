'''
class Config(object):
    """
    Common configurations
    """

    DEBUG = False
    TESTING = False
    #DB_SERVER = 'postgres_host'
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@postgres_host:5432/stage_db'

    #def SQLALCHEMY_DATABASE_URI(self):
    #    return 'postgresql://stage_test:1234abcd@{}:5432/stage_db'.format(self.DB_SERVER)   
'''

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@192.168.1.76:5432/stage_db'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False
    #DB_SERVER = 'postgres_host'
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@postgres_host:5432/stage_db'

class TestingConfig(Config):
    """
    testing configurations
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@192.168.1.76:5432/stage_db'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test':TestingConfig
}
