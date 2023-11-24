import os
from dotenv import load_dotenv
load_dotenv(override=True)

class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
        'user': 'root',
        'password': open('/run/secrets/db-password', 'r').read(),
        'host': 'db',
        'dbname': 'example'
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # logging.DEBUG でメールの内容を確認できます。
    # MAIL_DEBUG = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('nginx-flask-mysql', os.getenv('MAIL_USERNAME'))
    # MAIL_SUPPRESS_SEND : default app.testing
    # 実際のメール送信をしない場合は True に設定します。
    # MAIL_SUPPRESS_SEND = True

    # MAIL_ASCII_ATTACHMENTS : default False
    # 添付ファイル名をASCIIに変換するかどうか。

Config = DevConfig