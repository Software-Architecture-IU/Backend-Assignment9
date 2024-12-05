from multiprocessing import Process, Queue
from schemas import PostUserMessage
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


class Publisher(Process):
    def __init__(self, input: Queue, ack: Queue) -> None:
        super().__init__()
        self.input = input
        self.ack = ack

    def process(self, body: PostUserMessage):
        body = json.loads(body.model_dump_json())
        logging.info(f'Received message {body}')
        brothers = ["m.korinenko@innopolis.university"]

        send_email('mail.innopolis.ru', 587, os.getenv('EMAIL_SENDER'),
                   os.getenv('EMAIL_PASSWORD'),
                   brothers, "IU SA Assignment #9", format_json_to_msg(body))

        self.ack.put(True)

    def run(self) -> None:
        while True:
            body = self.input.get()
            if body is None:
                break
            self.process(body)
