from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

from metatracker import CONFIGURATION
from metatracker.database import create_engine, create_session
from metatracker.database.tables import (
    create_table,
    create_tables,
    get_columns,
    get_tables,
    remove_tables,
    table_exists,
)

MISSION_NAME = CONFIGURATION.mission_name


def test_get_tables():
    # Create engine and session
    engine = create_engine("sqlite://")

    # Create Base
    Base = declarative_base()

    # Create dummy table class
    class TestTable(Base):
        __tablename__ = "test_table"
        test_id = Column(Integer, primary_key=True)

    # Set up tables
    create_table(engine=engine, table_class=TestTable)

    # Get tables
    tables = get_tables(engine=engine)

    assert "test_table" in tables


def test_get_columns():
    # Create engine and session
    engine = create_engine("sqlite://")

    # Create Base
    Base = declarative_base()

    # Create dummy table class
    class TestTable(Base):
        __tablename__ = "test_table"
        test_id = Column(Integer, primary_key=True)

    # Set up tables
    create_table(engine=engine, table_class=TestTable)

    # Get columns
    columns = get_columns(engine=engine, table_name="test_table")

    for column in columns:
        assert column["name"] == "test_id"
        assert column["primary_key"] == 1


def test_create_table():
    # Create engine and session
    engine = create_engine("sqlite://")

    # Create Base
    Base = declarative_base()

    # Create dummy table class
    class TestTable(Base):
        __tablename__ = "test_table"
        test_id = Column(Integer, primary_key=True)

    # Set up tables
    create_table(engine=engine, table_class=TestTable)

    # Get tables
    created_tables = get_tables(engine=engine)

    assert "test_table" in created_tables


def test_table_exists():
    # Create engine and session
    engine = create_engine("sqlite://")

    # Create Base
    Base = declarative_base()

    # Create dummy table class
    class TestTable(Base):
        __tablename__ = "test_table"
        test_id = Column(Integer, primary_key=True)

    # Set up tables
    create_table(engine=engine, table_class=TestTable)

    # Get tables
    created_tables = get_tables(engine=engine)

    assert "test_table" in created_tables


def test_create_tables():
    # Create engine and session
    engine = create_engine("sqlite://")
    create_session(engine)

    # Set up tables
    create_tables(engine=engine)

    # Expected tables
    table_names = [
        f"{MISSION_NAME}_file_level",
        f"{MISSION_NAME}_instrument_configuration",
        f"{MISSION_NAME}_instrument",
        f"{MISSION_NAME}_file_type",
        f"{MISSION_NAME}_science_file",
        f"{MISSION_NAME}_science_product",
        f"{MISSION_NAME}_status",
    ]

    # Get tables
    created_tables = get_tables(engine=engine)

    # Sort the tables
    table_names.sort()
    created_tables.sort()

    # Test expected tables and the returned tables are the same
    assert created_tables == table_names


def test_create_tables_existing():
    # Create engine and session
    engine = create_engine("sqlite://")
    create_session(engine)

    # Set up tables
    create_tables(engine=engine)

    # Expected tables
    table_names = [
        f"{MISSION_NAME}_file_level",
        f"{MISSION_NAME}_instrument_configuration",
        f"{MISSION_NAME}_instrument",
        f"{MISSION_NAME}_file_type",
        f"{MISSION_NAME}_science_file",
        f"{MISSION_NAME}_science_product",
        f"{MISSION_NAME}_status",
    ]

    # Get tables
    created_tables = get_tables(engine=engine)

    # Sort the tables
    table_names.sort()
    created_tables.sort()

    # Test expected tables and the returned tables are the same
    assert created_tables == table_names

    # Retry without error
    create_tables(engine=engine)


def test_remove_tables():
    # Create engine and session
    engine = create_engine("sqlite://")

    # Set up tables
    create_tables(engine=engine)

    # Expected tables
    table_names = [
        f"{MISSION_NAME}_file_level",
        f"{MISSION_NAME}_instrument_configuration",
        f"{MISSION_NAME}_instrument",
        f"{MISSION_NAME}_file_type",
        f"{MISSION_NAME}_science_file",
        f"{MISSION_NAME}_science_product",
        f"{MISSION_NAME}_status",
    ]

    # Get tables
    created_tables = get_tables(engine=engine)

    # Sort the tables
    table_names.sort()
    created_tables.sort()

    # Test expected tables and the returned tables are the same
    assert created_tables == table_names

    # Remove tables
    remove_tables(engine=engine)

    # Get tables
    assert not table_exists(engine=engine, table_name=f"{MISSION_NAME}_file_level")
