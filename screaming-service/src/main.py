import json
import logging
import threading

from rabbitmq import rabbitmq_producer, rabbitmq_consumer
from transformer import scream


def start_heartbeat():
    rabbitmq_producer.send_heartbeat()
    threading.Timer(10, start_heartbeat).start()


def process_and_send(ch, method, properties, body) -> None:
    body = json.loads(body.decode())
    logging.info(f'Received message {body}')
    proceeded_body = scream(body)

    rabbitmq_producer.publish_message(json.dumps(proceeded_body))


if __name__ == '__main__':
    start_heartbeat()
    rabbitmq_consumer.consume(process_and_send)
