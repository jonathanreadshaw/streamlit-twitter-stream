from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from database import Base


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    body = Column(String(1000), nullable=False)
    keyword = Column(String(256), nullable=False)
    tweet_date = Column(DateTime, nullable=False)
    location = Column(String(100))
    verified_user = Column(Boolean)
    followers = Column(Integer)
    sentiment = Column(Float)

    def __init__(self, body, keyword, tweet_date, location, verified_user, followers, sentiment):
        self.body = body
        self.keyword = keyword
        self.tweet_date = tweet_date
        self.location = location
        self.verified_user = verified_user
        self.followers = followers
        self.sentiment = sentiment

    def __repr__(self):
        return '<Tweet %r>' % self.body
