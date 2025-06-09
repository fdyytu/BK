from kafka import KafkaProducer, KafkaConsumer
from typing import Any, Callable, Optional
from .base import BaseQueue

class KafkaQueue(BaseQueue):
    """
    Kafka queue provider implementation.
    """

    def __init__(self, hosts: list, topic_prefix: str = ""):
        self.hosts = hosts
        self.topic_prefix = topic_prefix
        self.producer = None
        self.consumer = None

    def connect(self) -> None:
        self.producer = KafkaProducer(bootstrap_servers=self.hosts)

    def publish(self, queue: str, message: Any, **kwargs) -> None:
        topic = f"{self.topic_prefix}{queue}"
        self.producer.send(topic, str(message).encode('utf-8'))
        self.producer.flush()

    def consume(self, queue: str, callback: Callable, **kwargs) -> None:
        topic = f"{self.topic_prefix}{queue}"
        self.consumer = KafkaConsumer(topic, bootstrap_servers=self.hosts, auto_offset_reset='earliest')
        for msg in self.consumer:
            callback(msg.value.decode('utf-8'))

    def close(self) -> None:
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()