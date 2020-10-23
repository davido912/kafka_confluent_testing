from confluent_kafka import Consumer

broker_endpoint = "localhost:9092"

def create_consumer():
    c = Consumer({"bootstrap.servers": broker_endpoint,
                  "group.id": "test_group_4",
                  # "auto.offset.reset": "earliest",
                  "enable.auto.commit": False
                  })
    c.subscribe(['david_test_poc_kafka'])
    return c


def consume():
    consumer = create_consumer()
    while True:
        msg = consumer.poll()

        if msg is None:
            break
        if msg.error():
            print("error")
            continue
        print(msg.value().decode('utf-8'))


if __name__ == '__main__':
    consume()