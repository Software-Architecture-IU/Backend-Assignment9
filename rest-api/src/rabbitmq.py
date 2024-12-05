import logging
import time

import pika

from config import config

PRINT_MESSAGE_SIZE = 128


class RabbitMQProducer:
    def __init__(self, host='localhost', port=5672, user='guest', password='guest', queue_name='default_queue'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        retry_intervals = [5000, 10000, 15000]
        for attempt, wait_time in enumerate(retry_intervals, start=1):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                                    credentials=pika.PlainCredentials(
                                                                                        self.user, self.password),
                                                                                    heartbeat=15))

                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name, durable=True, auto_delete=False)

                logging.info(f'Connected to RabbitMQ on host: {self.host}; Synchronized with queue: {self.queue_name}')

                return

            except Exception as e:
                logging.error(f"Error connecting to RabbitMQ: {e}")
                if attempt < len(retry_intervals):
                    logging.info(f'Retrying connect number {attempt}...')
                    time.sleep(wait_time / 1000)

        logging.critical("Failed to connect to RabbitMQ after multiple attempts.")

    def publish_message(self, message: str):
        if self.channel is None:
            logging.info(f'The connection with the RabbitMQ (host: {self.host}) is not established yet')
            return

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
            logging.info(
                f"Sent message to the queue {self.queue_name} with the content: {message[:PRINT_MESSAGE_SIZE]}")
        except Exception as e:
            logging.error(f"Error publishing message: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info(f'Connection to RabbitMQ(host: {self.host}) is closed')

    def send_heartbeat(self):
        if not self.connection or not self.connection.is_open:
            logging.info('Connection to RabbitMQ is not established or is closed. Attempting to reconnect...')
            self.connect()

        if self.connection and self.connection.is_open:
            try:
                self.connection.process_data_events()
            except Exception as e:
                logging.error(f"Error sending heartbeat: {e}")
        else:
            logging.error('Cannot connect to the RabbitMQ; Heartbeat cannot be sent')


class RabbitMQConsumer:
    def __init__(self, host='localhost', port=5672, user='guest', password='guest',
                 queue_name="publish_service--rest_service--queue"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        retry_intervals = [5000, 10000, 15000]
        for attempt, wait_time in enumerate(retry_intervals, start=1):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                                    credentials=pika.PlainCredentials(
                                                                                        self.user, self.password),
                                                                                    heartbeat=15))

                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name, durable=True, auto_delete=False)

                logging.info(f'Connected to RabbitMQ on host: {self.host}; Synchronized with queue: {self.queue_name}')

                return

            except Exception as e:
                logging.error(f"Error connecting to RabbitMQ: {e}")
                if attempt < len(retry_intervals):
                    logging.info(f'Retrying connect number {attempt}...')
                    time.sleep(wait_time / 1000)

        logging.critical("Failed to connect to RabbitMQ after multiple attempts.")

    def consume_one_message(self) -> str:
        """
        Consume a single message in blocking mode.
        """
        if not self.channel:
            logging.error("Channel is not initialized. Did you forget to call connect()?")
            return None

        method_frame, properties, body = self.channel.basic_get(queue=self.queue_name, auto_ack=False)

        if method_frame:
            logging.info(f"Received message: {body}")
            
            # Acknowledge the message to remove it from the queue
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return body
        else:
            logging.info("No message available in the queue.")
            return None

    def consume(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        logging.info(f'Waiting for messages on {self.queue_name}')
        try:
            self.channel.start_consuming()
        except Exception as any:
            logging.error(f"Error waiting for messages on {self.queue_name} -- {any}")
        finally:
            self.close()

    def close(self):
        if self.connection:
            self.connection.close()
        if self.connection:
            self.connection.close()
            logging.info(f'Connection to RabbitMQ(host: {self.host}) is closed')


rabbitmq_producer = RabbitMQProducer(config['rabbitmq']['host'], config['rabbitmq']['port'], config['rabbitmq']['user'],
                                     config['rabbitmq']['password'], config['rabbitmq']['queue-to-produce'])
rabbitmq_producer.connect()

rabbitmq_consumer = RabbitMQConsumer(config['rabbitmq']['host'], config['rabbitmq']['port'], config['rabbitmq']['user'],
                                     config['rabbitmq']['password'], config['rabbitmq']['queue-to-consume'])
rabbitmq_consumer.connect()
