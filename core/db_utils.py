import os

from sqlalchemy import create_engine


def engine():
    db_url = os.environ.get('DATABASE_URL')
    return create_engine(db_url)
