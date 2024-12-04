# File Type Table
# Schema:
#   short_name: str (primary key)
#   full_name: str
#   description: str

from sqlalchemy import Column, String

from metatracker import CONFIGURATION

from . import base_table as Base


class FileTypeTable(Base.Base):
    # Name Of Table
    __tablename__ = f"{CONFIGURATION.mission_name}_file_type"

    # Short Name Of File Type
    short_name = Column(String, primary_key=True)

    # Full Name Of File Type
    full_name = Column(String)

    # Description Of File Type
    description = Column(String)

    # Extension Of File Type
    extension = Column(String)

    def __init__(self, short_name: str, full_name: str, description: str, extension: str) -> None:
        """
        Constructor for File Type Table
        """
        self.short_name = short_name
        self.full_name = full_name
        self.description = description
        self.extension = extension

    def __repr__(self) -> str:
        return super().__repr__()


def return_class() -> type:
    """
    Return Class
    """
    return FileTypeTable
