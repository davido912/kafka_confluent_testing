from confluent_kafka.admin import AdminClient, NewTopic
from custom_logger import custom_logger

logger = custom_logger()

kafka_broker_endpoint = 'localhost:9092'
kafka_client = AdminClient({"bootstrap.servers": kafka_broker_endpoint})

kafka_topics = ["test_kafka_poc_david"]


def create_topics(topic_names: list):
    test_topic = [NewTopic(topic=topic, num_partitions=2, replication_factor=2) for topic in topic_names]
    result = kafka_client.create_topics(new_topics=test_topic, validate_only=False, operation_timeout=50)

    for topic, res in result.items():
        try:
            res.result()
            logger.info(result)
            logger.info("TOPIC %s CREATED" % topic)
        except Exception as e:
            logger.error("FAILED TO CREATE TOPIC: %s" % e)


def delete_topics(topic_names: list):
    result = kafka_client.delete_topics(topics=topic_names)

    for topic, res in result.items():
        try:
            res.result()
            logger.info("TOPIC %s DELETED" % topic)
        except Exception as e:
            logger.error("FAILED TO DELETE TOPIC: %s" % e)


if __name__ == "__main__":
    create_topics(kafka_topics)
#     delete_topics(kafka_topics)
