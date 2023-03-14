# Instrument Configuration Table
# Schema:
#   instrument_configuration_id: int (primary key)
#   instrument_{i+1}_id: int (foreign key)

from base_table import Base
from sqlalchemy import Column, Integer

from cdftracker import CDFTRACKER_CONFIG


def return_class() -> type:
    """
    Create Instrument Configuration Table
    """
    table_dict = {
        "__tablename__": f"{CDFTRACKER_CONFIG['mission_name']}_instrument_configuration",
        "instrument_configuration_id": Column(Integer, primary_key=True),
    }

    for i in range(len(CDFTRACKER_CONFIG["instruments"])):
        table_dict[f"instrument_{i+1}_id"] = Column(Integer)

    InstrumentConfigurationTable = type("InstrumentConfigurationTable", (Base,), table_dict)

    return InstrumentConfigurationTable


def return_table() -> type:
    """
    Create Instrument Configuration Table
    """

    return return_class().__table__
