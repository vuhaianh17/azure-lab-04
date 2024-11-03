import logging
import time
from datetime import datetime
import psycopg2
import azure.functions as func

# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail, Email, To, Content

DATABASE_NAME = "techconfdb"
DB_USER = "azureuser"
DB_PASSWORD = "098poiaA@"
DB_CONNECTION_STRING = (
    "host=azurelab.postgres.database.azure.com port=5432 dbname="
    + DATABASE_NAME
    + " user="
    + DB_USER
    + " password="
    + DB_PASSWORD
    + " sslmode=require"
)


def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode("utf-8"))
    logging.info(
        "Python ServiceBus queue trigger processed message: %s", notification_id
    )

    connection = psycopg2.connect(DB_CONNECTION_STRING)

    try:
        curr = connection.cursor()
        notification = getNotificationById(notification_id, curr)
        attendees = getAllAttendeesEmailAndName(curr)
        success_email = sendEmail(attendees, notification)
        updateNotificationTable(notification_id, success_email, curr)

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if connection:
            curr.close()
            connection.close()


def getNotificationById(id, curr):
    logging.info("Start getNotificationById")
    sql = f"SELECT * FROM notification WHERE notification.id = {id}"
    try:
        curr.execute(sql)
        data = curr.fetchall()
    except Exception as e:
        logging.error("Error when get notification by ID")
    return data


def getAllAttendeesEmailAndName(curr):
    logging.info("Start getAllAttendeesEmailAndName")
    sql = """SELECT email, first_name, last_name FROM attendee"""
    curr.execute(sql)
    return curr.fetchall()


def sendEmail(attendees, notification):
    logging.info("Start sendEmail")
    success = 0
    for attendee in attendees:
        try:
            time.sleep(20)
            success += 1
        except Exception as e:
            logging.error("Error when send notification for email %s", attendee[0])
    return success


def updateNotificationTable(id, number_of_success, curr):
    logging.info("Start updateNotificationTable")
    logging.info("status = Notified ... attendees")
    status = f"Notified {number_of_success} attendees"
    finish_time = f"{datetime.utcnow()}"
    sql = """UPDATE notification """
    sql = sql + """SET status = '""" + status + """' , completed_date = '""" + finish_time
    sql = sql + """' WHERE id = """ + f"{id}"
    curr.execute(sql)