import datetime
import json
import random
import uuid
from typing import Any

from kafka import KafkaProducer


def create_producer(server_address: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[server_address],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def publish_message(producer: KafkaProducer, topic: str, message: Any) -> None:
    producer.send(topic, message)
    producer.flush()
    return None


def close_producer(producer: KafkaProducer) -> None:
    producer.close()
    return None


def sample_data():
    return {
        "uid": str(uuid.uuid4()),
        "timestamp": str(datetime.datetime.now()),
        "value": random.random(),
    }


if __name__ == "__main__":
    import os

    ADDRESS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
    TOPIC = os.environ.get("KAFKA_TOPIC", "")

    producer = create_producer(ADDRESS)
    for i in range(1000):
        print(i)
        publish_message(
            producer=producer,
            topic=TOPIC,
            message=sample_data(),
        )
    close_producer(producer)
