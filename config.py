class BaseConfig:
    USER_DB = 'postgres'
    PASS_DB = 'admin'
    URL_DB  = 'localhost'
    NAME_DB = 'proyecto'
    FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
    SQLALCHEMY_DATABASE_URI = FULL_URL_DB
    SECRET_KEY = 'XDECDCL393D9J@'
    DEBUG = False
    BCRYPT_LOG_ROUND = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False