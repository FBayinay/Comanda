class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://fbayinay:159753@postgres:5432/comanda"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False