import json
import logging

from config import config
from rabbitmq import rabbitmq_consumer, rabbitmq_producer
from sender import send_email
from datetime import datetime


def format_json_to_msg(jsn: json) -> str:
    string = ''
    for key, value in jsn.items():
        string += key + ': ' + value
        string += '\n'
    return string


def process_and_send_email(ch, method, properties, body) -> None:
    body = json.loads(body.decode('utf-8'))
    logging.info(f'Received message {body}')

    send_email(config['email']['server'], config['email']['port'], config['email']['user'], config['email']['password'],
               config['email']['team_members'], config['email']['subject'], format_json_to_msg(body))
    rabbitmq_producer.publish_message(str(datetime.now().timestamp()))


if __name__ == '__main__':
    rabbitmq_consumer.consume(process_and_send_email)
