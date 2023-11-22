class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
        'user': 'root',
        'password': open('/run/secrets/db-password', 'r').read(),
        'host': 'db',
        'dbname': 'example'
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

Config = DevConfig