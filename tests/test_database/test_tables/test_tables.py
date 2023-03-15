from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

from cdftracker import MISSION_NAME
from cdftracker.database import create_engine, create_session
from cdftracker.database.tables import create_table, get_columns, get_tables, set_up_tables


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


def test_set_up_tables():
    # Create engine and session
    engine = create_engine("sqlite://")
    session = create_session(engine)

    # Set up tables
    set_up_tables(engine=engine, session=session)

    # Expected tables
    table_names = [
        f"{MISSION_NAME}_file_level",
        f"{MISSION_NAME}_instrument_configuration",
        f"{MISSION_NAME}_instrument",
        f"{MISSION_NAME}_file_type",
        f"{MISSION_NAME}_science_file",
        f"{MISSION_NAME}_science_product",
    ]

    # Get tables
    created_tables = get_tables(engine=engine)

    # Sort the tables
    table_names.sort()
    created_tables.sort()

    # Test expected tables and the returned tables are the same
    assert created_tables == table_names
