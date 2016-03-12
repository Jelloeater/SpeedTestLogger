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
from sqlalchemy import Column, Integer, String

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
class Device(BASE):
    """Defines Device object relational model, is used for both table creation and object interaction"""
    __tablename__ = 'Device'
    device_id = Column('device_id', Integer, primary_key=True)
    username = Column('username', String, nullable=False)
    password = Column('password', String, nullable=False)
    enable_password = Column('enable_password', String, nullable=False)
    hostname = Column('hostname', String, nullable=False)
    config_file = Column('config_file', String, nullable=False)

    # Helper methods
    @staticmethod
    def get_devices():
        session = get_session()
        return session.query(Device).all()

    # @staticmethod
    # def add_device(username, ssh_password, enable_password, hostname, config_dump_file):
    #     session = get_session()
    #     new_device = Device()
    #     new_device.username = username
    #     new_device.password = ssh_password
    #     new_device.enable_password = enable_password
    #     new_device.hostname = hostname
    #     new_device.config_file = config_dump_file
    #     session.add(new_device)
    #     session.commit()

    @staticmethod
    def get_number_of_devices():
        return get_session().query(Device).count()


# # Defines Log ORM
# class Log(BASE):
# __tablename__ = 'Log'
#     log_id = Column('log_id', Integer, primary_key=True)
#     device_id = Column('device_id', None, ForeignKey('Device.device_id'))
#     timestamp = Column('timestamp', TIMESTAMP, nullable=False)


class Setup:
    def __init__(self):
        pass

    @staticmethod
    def setup_sql_environment():
        try:
            Setup.create_db()
        except pg8000.core.ProgrammingError:
            logging.debug('Database Already Present')

        logging.debug('Creating table if not already present')
        Setup.create_tables()

    @staticmethod
    def create_db():
        conn = pg8000.connect(host=settings.DB_host, user=settings.DB_user, password=settings.DB_password)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE asapull")
        conn.autocommit = False
        cur.close()
        conn.close()

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
