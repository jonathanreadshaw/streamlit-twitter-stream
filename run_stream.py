import os, logging, datetime, argparse
from logging.handlers import RotatingFileHandler
from config import TwitterConfig
from stream import TweetListener
from tweepy import Stream
from tweepy import OAuthHandler

log_dir = 'Logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_name = 'streaming_{}.log'.format(datetime.date.today().strftime('%Y%m%d'))
log_handler = RotatingFileHandler(filename=os.path.join(log_dir, log_name), maxBytes=20000, backupCount=5)
logging.basicConfig(handlers=[log_handler], level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S')


def parse_args():
    parser = argparse.ArgumentParser(description='Database twitter streams.')
    parser.add_argument("-k", "--keywords", type=str, required=True,
                        help="Keywords to filter stream (comma seperated, wrap in quotation marks")
    args = parser.parse_args()
    return args


def run():
    auth = OAuthHandler(TwitterConfig.CONSUMER_KEY, TwitterConfig.CONSUMER_SECRET)
    auth.set_access_token(TwitterConfig.ACCESS_TOKEN, TwitterConfig.ACCESS_TOKEN_SECRET)
    keywords = parse_args().keywords.split(',')
    keywords = [word.strip(' ') for word in keywords]
    listener = TweetListener(keywords)
    stream = Stream(auth, listener)
    logging.info('Starting stream: {}'.format(keywords[0]))
    stream.filter(track=keywords, languages=['en'])
    logging.info('Stream closed')


if __name__ == '__main__':
    run()
