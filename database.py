from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from config import DBConfig

engine = create_engine('mysql+pymysql://{}:{}@{}/twitter_sqlalc'.format(DBConfig.USER, DBConfig.PWORD, DBConfig.HOST),
                       convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    Base.metadata.create_all(bind=engine)
