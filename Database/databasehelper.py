import datetime
import logging
import os
import platform

from prometheus_client import Counter
from sqlalchemy import Column, TIMESTAMP, FLOAT, INTEGER, inspect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

__author__ = 'jesse'

# Global ORM BASE, used by module
BASE = declarative_base()
SQL_LITE_DB_NAME = 'Speed' + '.db'
SQL_LITE_ENGINE_URL = 'sqlite:///' + SQL_LITE_DB_NAME


DB_ENGINE_ACCESS_COUNTER = Counter('db_engine_access_counter', 'Number of DB Engine Calls')

def get_engine():
    """Returns SQL engine depending on OS"""
    if platform.system() == 'Windows':
        engine_url = SQL_LITE_ENGINE_URL
    else:
        SQL_HOSTNAME = os.environ['SQL_HOSTNAME']
        SQL_USERNAME = os.environ['SQL_USERNAME']
        SQL_PASSWORD = os.environ['SQL_PASSWORD']
        SQL_PORT = os.environ['SQL_PORT']
        SQL_DB = os.environ['SQL_DB']
        engine_url = 'postgresql://' + SQL_USERNAME + ':' + SQL_PASSWORD + '@' + SQL_HOSTNAME + ':' + SQL_PORT + '/' + SQL_DB

    engine = create_engine(engine_url)
    DB_ENGINE_ACCESS_COUNTER.inc()
    return engine



def get_session():
    engine = get_engine()
    BASE.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


class Setup:
    def __init__(self):
        pass

    @staticmethod
    def setup_sql_environment():
        logging.debug('Checking SQL Enviroment...')
        Setup.create_db()
        Setup.create_tables()

    @staticmethod
    def create_db():
        engine = get_engine()
        if not database_exists(engine.url):
            create_database(engine.url)
            logging.info('DB INITIALIZED')
        else:
            logging.debug('DB PRESENT')

    @staticmethod
    def create_tables():
        engine = get_engine()
        logging.debug(os.getcwd())
        logging.debug(os.path.dirname(os.path.abspath(__file__)))

        # check table exists
        ins = inspect(engine)
        if 'SpeedTestData' not in ins.get_table_names():
            BASE.metadata.drop_all(engine)
            BASE.metadata.create_all(engine)
            logging.info('TABLE INITIALIZED')
        else:
            logging.debug('TABLE PRESENT')


# Classes are directly mapped to tables,
# without the need for a mapper binding (ex mapper(Class, table_definition))
class SpeedTestData(BASE):
    """Defines Device object relational model,
    is used for both table creation and object interaction"""
    __tablename__ = 'SpeedTestData'
    item_id = Column('item_id', INTEGER, primary_key=True)
    timestamp = Column('timestamp', TIMESTAMP, nullable=False)
    up_speed = Column('up_speed', FLOAT, nullable=False)
    down_speed = Column('down_speed', FLOAT, nullable=False)
    ping = Column('ping', FLOAT, nullable=False)

    # Helper methods
    @staticmethod
    def get_all_data():
        session = get_session()
        return session.query(SpeedTestData).all()

    @staticmethod
    def get_x_days(num_of_days):
        session = get_session()
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=num_of_days)
        return session.query(SpeedTestData).filter(
            SpeedTestData.timestamp.between(start_date, end_date)).all()

    @staticmethod
    def put_data(speed_data):
        data = SpeedTestData()
        data.timestamp = datetime.datetime.now()
        data.up_speed = speed_data.uploadResult
        data.down_speed = speed_data.downloadResult
        data.ping = speed_data.pingResult
        s = get_session()
        s.add(data)
        s.commit()
