from multiprocessing import Queue
from schemas import PostUserMessage
from base import BaseFilter
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os


def send_email(smtp_server, port, username, password, recipients, subject,
               message_body):
    try:
        mail = MIMEMultipart()
        mail['From'] = username
        mail['Subject'] = subject

        mail.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)

            for recipient in recipients:
                mail['To'] = recipient
                server.sendmail(username, recipient, mail.as_string().encode('utf-8'))
            logging.info(f'Email sent to all the recipients: {recipients}')

    except Exception as e:
        logging.error(f"An error occurred: {e}")


def format_json_to_msg(jsn: json) -> str:
    string = ''
    for key, value in jsn.items():
        string += key + ': ' + value
        string += '\n'
    return string


class Publisher(BaseFilter):
    def __init__(self, input: Queue[PostUserMessage]) -> None:
        super().__init__()
        self.input = input

    def process(self, body: PostUserMessage):
        body = json.loads(body.decode('utf-8'))
        logging.info(f'Received message {body}')
        brothers = ["a.mukhutdinov@innopolis.university",
                    "m.korinenko@innopolis.university",
                    "d.nikulin@innopolis.university",
                    "m.kamenetskii@innopolis.university"]

        send_email('mail.innopolis.ru', 587, os.getenv('EMAIL_SENDER'),
                   os.getenv('EMAIL_PASSWORD'),
                   brothers, "IU SA Assignment #9", format_json_to_msg(body))