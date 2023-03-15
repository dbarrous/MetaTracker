# Instrument Configuration Table
# Schema:
#   instrument_configuration_id: int (primary key)
#   instrument_{i+1}_id: int (foreign key)

from sqlalchemy import Column, Integer

from cdftracker import INSTRUMENTS, MISSION_NAME

from . import base_table as Base

table_dict = {
    "__tablename__": f"{MISSION_NAME}_instrument_configuration",
    "instrument_configuration_id": Column(Integer, primary_key=True),
}

for i in range(len(INSTRUMENTS)):
    table_dict[f"instrument_{i+1}_id"] = Column(Integer)

InstrumentConfigurationTable = type("InstrumentConfigurationTable", (Base.Base,), table_dict)


def return_class() -> type:
    """
    Return Class
    """
    return InstrumentConfigurationTable
