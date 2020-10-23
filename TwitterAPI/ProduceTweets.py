from kafka_producer import create_producer
import tweepy
from TwitterAPI.TwitterHook import twitter_api_hook
from custom_logger import custom_logger
from utils.yaml_parsing import parse_yaml_file
import json
import atexit
import signal
import sys

logger = custom_logger()


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, kafka_producer):
        super().__init__()
        self.producer = kafka_producer
        self.tweets_count = 0

    def on_status(self, status):
        self.producer.produce(topic="david_test_poc_kafka", value=json.dumps(status._json))
        logger.info(status._json)
        self.tweets_count += 1
        atexit.register(self.on_exit)

    def on_data(self, raw_data):
        super().on_data(raw_data)

    def on_exit(self):
        self.producer.flush() # flush all msgs on exit


def produce_tweets_to_kafka(track_keywords: list):
    credential_fpath = '/Users/dohayon/PycharmProjects/pythonProject/credentials/credentials.yaml'
    twitter_api_creds = parse_yaml_file(credential_fpath)['twitter_credentials']
    logger.info(twitter_api_creds)

    twitter_hook = twitter_api_hook(twitter_api_creds)
    kafka_producer = create_producer()
    twitter_stream_listener = TwitterStreamListener(kafka_producer=kafka_producer)

    stream = tweepy.Stream(auth=twitter_hook.auth,
                           listener=twitter_stream_listener)

    def _signal_handler(sig, frame):
        logger.info("TOTAL TWEETS PULLED: %s" % twitter_stream_listener.tweets_count)
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)
    stream.filter(track=track_keywords)



produce_tweets_to_kafka(['trump'])


