import os
import datetime

__author__ = 'jesse'
from sqlalchemy.orm import sessionmaker


# from sqlalchemy.dialects.postgresql import \
# ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
# DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
# INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
# TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
# DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR
# http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html

# NOTE This is only to be used with pure SQLalchemy, not FAB
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, FLOAT, INTEGER

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import logging

# Global ORM BASE, used by module
BASE = declarative_base()


def get_engine():
    return create_engine('sqlite:///SpeedData.db')

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
        logging.debug('Creating table if not already present')
        Setup.create_tables()

    @staticmethod
    def create_tables():
        engine = get_engine()
        if not os.path.isfile('SpeedData.db'):
            BASE.metadata.drop_all(engine)
            BASE.metadata.create_all(engine)
            logging.info('DATABASE INITIALIZED')
        else:
            logging.info('DATABASE PRESENT')

# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))
class SpeedTestData(BASE):
    """Defines Device object relational model, is used for both table creation and object interaction"""
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
        s =get_session()
        s.add(data)
        s.commit()
