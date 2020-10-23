from confluent_kafka import Producer
from time import sleep

broker_endpoint = "localhost:9092"

def create_producer():
    return Producer({"bootstrap.servers": broker_endpoint,
                     "enable.idempotence": "true",
                     "acks": "-1",
                     "compression.type": "snappy",
                     "linger.ms": 20,
                     "batch.size": str(32*1024),
                     "max.in.flight.requests.per.connection": 5
                     })


if __name__ == "__main__":
    producer = create_producer()
    for n in range(0,11):
        producer.produce(topic="david_test_poc_kafka", value=str(n))
        producer.poll()
        sleep(3)
        