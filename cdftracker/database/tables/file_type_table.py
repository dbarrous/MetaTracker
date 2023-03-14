# File Type Table
# Schema:
#   short_name: str (primary key)
#   full_name: str
#   description: str

from base_table import Base
from sqlalchemy import Column, String

from cdftracker import CDFTRACKER_CONFIG


class FileTypeTable(Base):
    # Name Of Table
    __tablename__ = f"{CDFTRACKER_CONFIG['mission_name']}_file_type"

    # Short Name Of File Type
    short_name = Column(String, primary_key=True)

    # Full Name Of File Type
    full_name = Column(String)

    # Description Of File Type
    description = Column(String)

    def __init__(self, short_name: str, full_name: str, description: str) -> None:
        """
        Constructor for File Type Table
        """
        self.short_name = short_name
        self.full_name = full_name
        self.description = description

    def __repr__(self) -> str:
        return super().__repr__()


def return_table() -> type:
    """
    Create File Type Table
    """
    return FileTypeTable.__table__
