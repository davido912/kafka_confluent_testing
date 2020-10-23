import tweepy
from custom_logger import custom_logger
from utils.yaml_parsing import parse_yaml_file

logger = custom_logger()

credential_fpath = '/Users/dohayon/PycharmProjects/pythonProject/credentials/credentials.yaml'

def twitter_api_hook(credentials: dict):
    auth = tweepy.OAuthHandler(consumer_key=credentials['api_key'],
                               consumer_secret=credentials['api_secret_key'])
    auth.set_access_token(key=credentials['access_token'],
                          secret=credentials['access_token_secret'])

    return tweepy.API(auth, wait_on_rate_limit=True)


def pull_tweets(search_term: list):
    api = twitter_api_hook(parse_yaml_file(credential_fpath)['twitter_credentials'])
    total_tweets_pulled = 0
    for tweet in tweepy.Cursor(api.search, q=search_term, count=100).items(): # by default twitter pulls only up to a week
        total_tweets_pulled += 1
        logger.info(tweet._json)
        yield tweet

    logger.info("TOTAL TWEETS PULLED: %s" % total_tweets_pulled )

