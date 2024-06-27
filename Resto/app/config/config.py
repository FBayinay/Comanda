import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://fbayinay:159753@localhost/comanda')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
