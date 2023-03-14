# Instrument Table
# Schema:
#   instrument_id: int (primary key)
#   instrument_configuration_id: int (foreign key)
#   mode: str
#   reference_timestamp: datetime

from base_table import Base
from sqlalchemy import Column, Integer, String

from cdftracker import CDFTRACKER_CONFIG


class InstrumentTable(Base):
    # Name Of Table
    __tablename__ = f"{CDFTRACKER_CONFIG['mission_name']}_instrument"

    # ID Of Instrument (Primary Key)
    instrument_id = Column(Integer, primary_key=True)

    # Full Name Of Instrument
    full_name = Column(String)

    # Short Name Of Instrument
    short_name = Column(String)

    # Description Of Instrument
    description = Column(String)

    def __init__(self, instrument_id: int, full_name: str, short_name: str, description: str) -> None:
        """
        Constructor for Instrument Table
        """
        self.instrument_id = instrument_id
        self.full_name = full_name
        self.short_name = short_name
        self.description = description

    def __repr__(self) -> str:
        return super().__repr__()


def return_table() -> type:
    """
    Create File Type Table
    """
    return InstrumentTable.__table__
