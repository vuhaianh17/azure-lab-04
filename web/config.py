import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = True
    POSTGRES_URL = "azurelab.postgres.database.azure.com"
    POSTGRES_USER = "azureuser"
    POSTGRES_PW = "098poiaA@"
    POSTGRES_DB = "techconfdb"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                          db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LLuDIRhaJ8WCZQuip/A9QzGujtj4HrnAO+ASbIwnr8M='
    SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://azurebuslab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=LLuDIRhaJ8WCZQuip/A9QzGujtj4HrnAO+ASbIwnr8M='
    SERVICE_BUS_QUEUE_NAME = 'notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = ''  # Configuration not required, required SendGrid Account


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
