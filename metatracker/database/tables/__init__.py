"""
Setup Tables
"""

from sqlalchemy import inspect

from metatracker import CONFIGURATION, log
from metatracker.database import create_session

from . import file_level_table as FileLevelTable
from . import file_type_table as FileTypeTable
from . import instrument_configuration_table as InstrumentConfigurationTable
from . import instrument_table as InstrumentTable
from . import science_file_table as ScienceFileTable
from . import science_product_table as ScienceProductTable


def get_class_name(class_object: type) -> str:
    """
    Get Class Name

    :param class_object: Class Object
    :type class_object: type
    :return: Class Name
    :rtype: str
    """

    class_name = class_object.__name__

    return class_name


def get_table_modules() -> list:
    """
    Get Table Modules

    :return: List of Table Modules
    :rtype: list
    """

    modules = [
        FileLevelTable,
        FileTypeTable,
        InstrumentTable,
        InstrumentConfigurationTable,
        ScienceProductTable,
        ScienceFileTable,
    ]

    return modules


def get_table_classes(table_modules: list) -> list:
    """
    Get Table Classes

    :return: List of Table Classes
    :rtype: list
    """

    table_classes = [module.return_class() for module in table_modules]

    return table_classes


def get_table_from_class(table_class: type) -> type:
    """
    Get Table

    :param table_class: Table Class
    :type table_class: type
    :return: Table
    :rtype: type
    """

    table = table_class.__table__

    return table


def get_tables_from_classes(table_classes: list) -> list:
    """
    Get Tables from Table Classes

    :param table_classes: List of Table Classes
    :type table_classes: list
    :return: List of Tables
    :rtype: list
    """

    tables = [get_table_from_class(table_class) for table_class in table_classes]

    return tables


# Function to return all the tables in the database
def get_tables(engine: type) -> list:
    """
    Get Tables in Database

    :param engine: SQLAlchemy Engine
    :type engine: type
    :return: List of Tables
    :rtype: list
    """
    inspector = inspect(engine)

    return inspector.get_table_names()


# Function to check if a table exists in the database
def table_exists(engine: type, table_name: str) -> bool:
    """
    Check if Table Exists in Database

    :param engine: SQLAlchemy Engine
    :type engine: type
    :param table_name: Table Name
    :type table_name: str
    :return: Table Exists
    :rtype: bool
    """
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    return table_name in tables


# Function to get all columns in a table
def get_columns(engine: type, table_name: str) -> list:
    """
    Get Columns in Table in Database

    :param engine: SQLAlchemy Engine
    :type engine: type
    :param table_name: Table Name
    :type table_name: str
    :return: List of Columns
    :rtype: list
    """

    inspector = inspect(engine)

    return inspector.get_columns(table_name)


def populate_file_level_table(sql_session: type, file_levels: list, file_level_table: type) -> None:
    """
    Populate File Level Table

    :param sql_session: SQLAlchemy Session
    :type sql_session: sqlalchemy.orm.session.Session
    :param file_levels: List of file levels
    :type file_levels: list
    :param file_level_table: File Level Table
    :type file_level_table: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :return: None
    :rtype: None
    """
    log.info("Populating File Level Table")
    for file_level in file_levels:
        with sql_session.begin() as session:
            if session.query(file_level_table).filter_by(short_name=file_level["short_name"]).first() is None:
                log.info(f"Adding {file_level['short_name']} to File Level Table")
                session.add(
                    file_level_table(
                        full_name=file_level["full_name"],
                        short_name=file_level["short_name"],
                        description=file_level["description"],
                    )
                )
            else:
                log.info(f"{file_level['short_name']} already exists in File Level Table")


def populate_file_type_table(sql_session: type, file_types: list, file_level_table: type) -> None:
    """
    Populate File Type Table

    :param sql_session: SQLAlchemy Session
    :type sql_session: sqlalchemy.orm.session.Session
    :param file_types: List of file types
    :type file_types: list
    :param file_level_table: File Level Table
    :type file_level_table: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :return: None
    :rtype: None
    """
    log.info("Populating File Type Table")
    for file_type in file_types:
        with sql_session.begin() as session:
            if session.query(file_level_table).filter_by(short_name=file_type["short_name"]).first() is None:
                log.info(f"Adding {file_type['short_name']} to File Type Table")
                session.add(
                    file_level_table(
                        short_name=file_type["short_name"],
                        full_name=file_type["full_name"],
                        description=file_type["description"],
                        extension=file_type["extension"],
                    )
                )
            else:
                log.info(f"{file_type['short_name']} already exists in File Type Table")


def populate_instrument_table(sql_session: type, instruments: list, instrument_table: type) -> None:
    """
    Populate Instrument Table

    :param sql_session: SQLAlchemy Session
    :type sql_session: sqlalchemy.orm.session.Session
    :param instruments: List of instruments
    :type instruments: list
    :param instrument_table: Instrument Table
    :type instrument_table: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :return: None
    :rtype: None
    """
    log.info("Populating Instrument Table")
    for instrument in instruments:
        with sql_session.begin() as session:
            if session.query(instrument_table).filter_by(short_name=instrument["short_name"]).first() is None:
                log.info(f"Adding {instrument['short_name']} to Instrument Table")
                session.add(
                    instrument_table(
                        instrument_id=instrument["instrument_id"],
                        short_name=instrument["short_name"],
                        full_name=instrument["full_name"],
                        description=instrument["description"],
                    )
                )
            else:
                log.info(f"{instrument['short_name']} already exists in Instrument Table")


def populate_instrument_configuration_table(
    sql_session: type, instrument_configurations: list, instrument_configuration_table: type
) -> None:
    """
    Populate Instrument Configuration Table

    :param sql_session: SQLAlchemy Session
    :type sql_session: sqlalchemy.orm.session.Session
    :param instrument_configurations: List of instrument configurations
    :type instrument_configurations: list
    :param instrument_configuration_table: Instrument Configuration Table
    :type instrument_configuration_table: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :return: None
    :rtype: None
    """
    log.info("Populating Instrument Configuration Table")
    for _instrument_configuration in instrument_configurations:
        with sql_session.begin() as session:
            # Check if the id exists in the Instrument Configuration Table
            if (
                session.query(instrument_configuration_table)
                .filter_by(instrument_configuration_id=_instrument_configuration["instrument_configuration_id"])
                .first()
                is None
            ):
                log.info(
                    f"Adding {_instrument_configuration['instrument_configuration_id']} to Instrument Configuration"
                    " Table"
                )
                session.add(instrument_configuration_table(**_instrument_configuration))

            else:
                log.info(
                    f"Configuration with ID {_instrument_configuration['instrument_configuration_id']} already exists"
                    " in Instrument Configuration Table"
                )


# Function to create table if it doesn't exist and match the table class
def create_table(engine: type, table_class: type) -> None:
    """
    Function to create table if it doesn't exist and match the table class

    :param engine: SQLAlchemy
    :type engine: sqlalchemy.engine.base.Engine
    :param table_class: Table Class
    :type table_class: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :return: None
    :rtype: None
    """
    log.info(f"Creating {get_class_name(table_class)} Table if it doesn't exist")
    table_class.__table__.create(bind=engine, checkfirst=True)


def create_tables(engine: type) -> None:
    """
    Set up tables in the database if they don't exist and populate them

    :param engine: SQLAlchemy
    :type engine: sqlalchemy.engine.base.Engine
    :param session: SQLAlchemy Session
    :type session: sqlalchemy.orm.session.Session
    :return: None
    :rtype: None
    """

    # Create Session
    session = create_session(engine)

    # Get Table Modules
    table_modules = get_table_modules()

    # Get Table Classes
    table_classes = get_table_classes(table_modules)

    # Get Tables
    get_tables_from_classes(table_classes)

    # Populate Tables
    for table_class in table_classes:
        create_table(engine, table_class)

        if get_class_name(table_class) == "FileLevelTable":
            populate_file_level_table(session, CONFIGURATION.file_levels, table_class)

        elif get_class_name(table_class) == "FileTypeTable":
            populate_file_type_table(session, CONFIGURATION.file_types, table_class)

        elif get_class_name(table_class) == "InstrumentTable":
            populate_instrument_table(session, CONFIGURATION.instruments, table_class)

        elif get_class_name(table_class) == "InstrumentConfigurationTable":
            populate_instrument_configuration_table(session, CONFIGURATION.instrument_configurations, table_class)


def remove_tables(engine: type) -> None:
    """
    Remove all tables from the database

    :param engine: SQLAlchemy
    :type engine: sqlalchemy.engine.base.Engine
    :return: None
    :rtype: None
    """
    # Get Table Modules
    table_modules = get_table_modules()

    # Get Table Classes
    table_classes = get_table_classes(table_modules)

    # Reverse Table Classes
    table_classes.reverse()

    # Remove Tables
    for table_class in table_classes:
        log.info(f"Removing {get_class_name(table_class)} Table")
        table_class.__table__.drop(bind=engine, checkfirst=True)
