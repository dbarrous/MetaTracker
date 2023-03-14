# File Level Table
# Schema:
#   short_name: str (primary key)
#   full_name: str
#   description: str

from base_table import Base
from sqlalchemy import Column, String

from cdftracker import CDFTRACKER_CONFIG


class FileLevelTable(Base):
    # Name Of Table
    __tablename__ = f"{CDFTRACKER_CONFIG['mission_name']}_file_level"

    # Short Name Of File Level
    short_name = Column(String, primary_key=True)

    # Full Name Of File Level
    full_name = Column(String)

    # Description Of File Level
    description = Column(String)

    def __init__(self, full_name: str, short_name: str, description: str) -> None:
        """
        Constructor for File Level Table
        """
        self.full_name = full_name
        self.short_name = short_name
        self.description = description

    def __repr__(self) -> str:
        return super().__repr__()


def return_table() -> type:
    """
    Create File Type Table
    """
    return FileLevelTable.__table__
