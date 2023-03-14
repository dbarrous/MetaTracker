"""
Setup Tables
"""

import file_level_table as FileLevelTable
import file_type_table as FileTypeTable
import instrument_configuration_table as InstrumentConfigurationTable
import instrument_table as InstrumentTable
import science_file_table as ScienceFileTable
import science_product_table as ScienceProductTable
from base_table import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cdftracker import CDFTRACKER_CONFIG, log

table_classes = [
    FileLevelTable,
    FileTypeTable,
    InstrumentTable,
    ScienceProductTable,
    ScienceFileTable,
]

InstrumentConfigurationTableInstance = InstrumentConfigurationTable.return_class()

tables = [table_class.return_table() for table_class in table_classes]

tables.append(InstrumentConfigurationTableInstance.__table__)


def set_up(db_host: str = CDFTRACKER_CONFIG["db_host"]):
    # Create engine
    engine = create_engine(db_host)

    # Create session
    Session = sessionmaker(engine)

    log.info("Creating Tables if they don't exist")
    # Create tables if they don't exist
    Base.metadata.create_all(engine, tables=tables, checkfirst=True)

    # Populate File Level Table If It Is Empty
    for file_level in CDFTRACKER_CONFIG["file_levels"]:
        with Session.begin() as session:
            if (
                session.query(FileLevelTable.FileLevelTable).filter_by(short_name=file_level["short_name"]).first()
                is None
            ):
                log.info(f"Adding {file_level['short_name']} to File Level Table")
                session.add(
                    FileLevelTable.FileLevelTable(
                        file_level["full_name"], file_level["short_name"], file_level["description"]
                    )
                )
            else:
                log.info(f"{file_level['short_name']} already exists in File Level Table")

    log.info("Populating File Type Table")
    # Populate File Type Table If It Is Empty
    for file_type in CDFTRACKER_CONFIG["file_types"]:
        with Session.begin() as session:
            if session.query(FileTypeTable.FileTypeTable).filter_by(short_name=file_type["short_name"]).first() is None:
                log.info(f"Adding {file_type['short_name']} to File Type Table")
                session.add(
                    FileTypeTable.FileTypeTable(
                        file_type["short_name"], file_type["full_name"], file_type["description"]
                    )
                )
            else:
                log.info(f"{file_type['short_name']} already exists in File Type Table")

    log.info("Populating Instrument Table")
    # Populate Instrument Table If It Is Empty
    for instrument in CDFTRACKER_CONFIG["instruments"]:
        with Session.begin() as session:
            if (
                session.query(InstrumentTable.InstrumentTable)
                .filter_by(instrument_id=instrument["instrument_id"])
                .first()
                is None
            ):
                log.info(f"Adding {instrument['short_name']} to Instrument Table")
                session.add(
                    InstrumentTable.InstrumentTable(
                        instrument["instrument_id"],
                        instrument["full_name"],
                        instrument["short_name"],
                        instrument["description"],
                    )
                )
            else:
                log.info(f"{instrument['short_name']} already exists in Instrument Table")

    log.info("Populating Instrument Configuration Table")
    # Populate Instrument Configuration Table If It Is Empty
    for _instrument_configuration in CDFTRACKER_CONFIG["instrument_configurations"]:
        with Session.begin() as session:
            # Check if the id exists in the Instrument Configuration Table
            if (
                session.query(InstrumentConfigurationTableInstance)
                .filter_by(instrument_configuration_id=_instrument_configuration["instrument_configuration_id"])
                .first()
                is None
            ):
                session.add(InstrumentConfigurationTableInstance(**_instrument_configuration))

            else:
                log.info(
                    f"Configuration with ID {_instrument_configuration['instrument_configuration_id']} already exists"
                    " in Instrument Configuration Table"
                )


set_up()
