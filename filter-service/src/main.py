import json
import logging
import threading

from filter import filter_message
from rabbitmq import rabbitmq_producer, rabbitmq_consumer


def start_heartbeat():
    rabbitmq_producer.send_heartbeat()
    threading.Timer(10, start_heartbeat).start()


def filter_and_send(ch, method, properties, body) -> None:
    body = json.loads(body.decode())
    logging.info(f'Received message {body}')
    found_word = filter_message(body)

    if found_word is None:
        rabbitmq_producer.publish_message(json.dumps(body))
    else:
        logging.info(f'Skip message because of the stop-word: {found_word}')


if __name__ == '__main__':
    start_heartbeat()
    rabbitmq_consumer.consume(filter_and_send)
