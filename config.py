import os


class TwitterConfig:
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


class DBConfig:
    USER = os.environ.get('DB_USER')
    PWORD = os.environ.get('DB_PWORD')
    HOST = os.environ.get('DB_HOST')


if __name__ == '__main__':
    print(type(os.environ.get('CONSUMER_KEY')))