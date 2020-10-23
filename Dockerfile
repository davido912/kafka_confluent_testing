ARG BASE_PYTHON_IMAGE=INSERT_URI
FROM $BASE_PYTHON_IMAGE

USER root
RUN mkdir -p /opt/kafka_test
RUN chown raisin /opt/kafka_test -R

USER raisin

COPY --chown=raisin:raisin requirements.txt .
RUN pip3 install -r ./requirements.txt --user

WORKDIR /opt/kafka_test

COPY ./poc_kafka_consumer.py poc_kafka_consumer.py 
COPY ./poc_kafka_producer.py poc_kafka_producer.py 


ENV PYTHONPATH /opt/kafka_test/

CMD ["python3", "/opt/kafka_test/poc_kafka_producer.py"]
