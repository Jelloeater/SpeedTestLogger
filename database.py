import os

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
from sqlalchemy import Column, Integer, String, TIMESTAMP

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
        print('Are you sure to want to DROP ALL TABLES, this cannot be undone!')
        if raw_input('({0})>'.format('Type YES to continue')) == 'YES':
            BASE.metadata.drop_all(engine)
            BASE.metadata.create_all(engine)
            print('DATABASE RE-INITIALIZED')
        else:
            print('Skipping database re-initialization')


# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))
class SpeedTestData(BASE):
    """Defines Device object relational model, is used for both table creation and object interaction"""
    __tablename__ = 'SpeedTestData'
    item_id = Column('item_id', Integer, primary_key=True)
    timestamp = Column('timestamp', TIMESTAMP, nullable=False)
    up_speed = Column('up_speed', String, nullable=False)
    down_speed = Column('down_speed', String, nullable=False)
    ping = Column('ping', String, nullable=False)

    # Helper methods
    @staticmethod
    def get_data():
        session = get_session()
        return session.query(SpeedTestData).all()