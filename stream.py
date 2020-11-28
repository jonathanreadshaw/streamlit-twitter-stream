from database import session_scope, init_db
from models import Tweet
from tweepy.streaming import StreamListener
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)


class TweetListener(StreamListener):

    def __init__(self, keywords):
        StreamListener.__init__(self)
        init_db()
        self.keywords = keywords
        self.sentiment_model = SentimentIntensityAnalyzer()

    def on_status(self, status):
        if status.retweeted or 'RT @' in status.text:
            return
        if status.truncated:
            text = status.extended_tweet['full_text']
        else:
            text = status.text
        location = status.coordinates
        if location:
            location = str(status.coordinates['coordinates'])
        keyword = self.check_keyword(text)
        if not keyword:
            return
        sentiment = self.sentiment_model.polarity_scores(text).get('compound')
        if sentiment == 0:
            return
        tweet = Tweet(body=text, keyword=keyword, tweet_date=status.created_at, location=location,
                      verified_user=status.user.verified, followers=status.user.followers_count,
                      sentiment=sentiment)
        self.insert_tweet(tweet)

    def on_error(self, status_code):
        if status_code == 420:
            # Stream limit reached, need to close the stream
            logger.warning('Limit Reached. Closing stream ({})'.format(self.lead_keyword))
            return False
        logger.warning('Streaming error (status code {})'.format(status_code))

    def insert_tweet(self, tweet):
        try:
            with session_scope() as sess:
                sess.add(tweet)
        except Exception as e:
            logger.warning('Unable to insert tweet: {}'.format(e))

    def check_keyword(self, body):
        for keyword in self.keywords:
            if keyword in body:
                return keyword
        return None

