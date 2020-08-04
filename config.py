import os

# Public server configurations.
class Config(object):
    
    USE_DATABASE_TYPE           = "sqllite"
    SQLALCHEMY_DATABASE_URI     = "sqlite:///vehicles.db"
    SQLALCHEMY_TRACK_MODIFICATIONS  = False