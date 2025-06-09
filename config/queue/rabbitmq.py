import pika
from typing import Any, Callable, Optional
from .base import BaseQueue

class RabbitMQQueue(BaseQueue):
    """
    RabbitMQ queue provider implementation.
    """

    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    def connect(self) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()

    def publish(self, queue: str, message: Any, **kwargs) -> None:
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=str(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def consume(self, queue: str, callback: Callable, **kwargs) -> None:
        self.channel.queue_declare(queue=queue, durable=True)
        def _callback(ch, method, properties, body):
            callback(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=_callback)
        self.channel.start_consuming()

    def close(self) -> None:
        if self.connection:
            self.connection.close()