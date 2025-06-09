from .rabbitmq import RabbitMQQueue
from .kafka import KafkaQueue
from .redis_queue import RedisQueue
from .inmemory import InMemoryQueue

def get_queue_provider(config: dict):
    """
    Factory to get a queue provider based on config.
    Example config:
        {"type": "rabbitmq", "url": "..."}
        {"type": "kafka", "hosts": [...]}
        {"type": "redis", "host": "...", "port": 6379}
        {"type": "memory"}
    """
    queue_type = config.get("type")
    if queue_type == "rabbitmq":
        return RabbitMQQueue(config["url"])
    elif queue_type == "kafka":
        return KafkaQueue(config["hosts"])
    elif queue_type == "redis":
        return RedisQueue(config.get("host", "localhost"), config.get("port", 6379))
    elif queue_type == "memory":
        return InMemoryQueue()
    else:
        raise ValueError(f"Unsupported queue type: {queue_type}")