import os


class Config:
    # import secrets; secret.token_hex(16)  # argiuments (16) is optional.
    SECRET_KEY = '8e6880f71e7fb8ad8e502554b1e8a244'  # btter if set env for it as same as EMAIL and EMAIL_PASSWORD.

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
