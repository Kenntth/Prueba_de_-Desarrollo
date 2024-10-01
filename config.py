# config.py

class Config(object):
    """
    Common configurations
    """

    # Coloque aquí cualquier configuración que sea común en todos los entornos.
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    #DEBUG = Verdadero
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
