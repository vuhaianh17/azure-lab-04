from azure.servicebus import ServiceBusClient
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.secret_key = app.config.get('SECRET_KEY')

service_bus_client = ServiceBusClient.from_connection_string(conn_str=app.config.get('SERVICE_BUS_CONNECTION_STRING'),
                                                             logging_enable=True)
queue_client = service_bus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))

db = SQLAlchemy(app)

from . import routes
