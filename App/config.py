import json, os

CONFIG = None

environment = os.environ.get('ENV')
if environment == 'production' or environment == 'staging':
    CONFIG = {
        "DEBUG" : False,
        "JWT_ACCESS_TOKEN_EXPIRES": 7,
        "SECRET_KEY" : os.environ.get('SECRET_KEY'),
        "SQLALCHEMY_DATABASE_URI" : os.environ.get('SQLALCHEMY_DATABASE_URI'),
        "ENV":'production'
    }
else:
    with open('environment.staging.json') as config_file:
        CONFIG = json.load(config_file)
