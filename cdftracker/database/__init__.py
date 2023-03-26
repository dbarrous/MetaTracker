"""
Module to handle database operations
"""

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import sessionmaker


# Function to check if you can connect to the database with SQLAlchemy
def check_connection(engine: type) -> bool:
    """
    Check Connection

    :param engine: SQLAlchemy Engine
    :type engine: type
    :return: Connection Status
    :rtype: bool
    """

    return bool(engine.connect())


def create_engine(db_host: str) -> type:
    """
    Create Engine

    :param db_host: Database Host
    :type db_host: str
    :return: SQLAlchemy Engine
    :rtype: type
    """

    engine = sqlalchemy_create_engine(db_host)
    return engine


# Function to create a database session
def create_session(engine: type) -> type:
    """
    Create Session

    :param engine: SQLAlchemy Engine
    :type engine: type
    :return: SQLAlchemy Session
    :rtype: type
    """

    session = sessionmaker(bind=engine)
    return session


# Function to create a database
