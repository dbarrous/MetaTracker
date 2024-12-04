# Schema:
# science_file_id: int (Primary Key Auto Increment)
# science_product_id: int (Foreign Key)
# file_type: int (Foreign Key)
# file_level: int (Foreign Key)
# filename: str
# file_version: int
# file_size: int
# file_extension: str
# file_path: str
# file_size: int
# file_modified_timestamp: datetime
# is_public: bool


from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from metatracker import CONFIGURATION

from . import base_table as Base


class ScienceFileTable(Base.Base):
    # Name Of Table
    __tablename__ = f"{CONFIGURATION.mission_name}_science_file"

    # ID Of Science Product (Primary Key)
    science_file_id = Column(Integer, primary_key=True, autoincrement=True)

    # ID Of Science Product (Foreign Key)
    science_product_id = Column(Integer, ForeignKey(f"{CONFIGURATION.mission_name}_science_product.science_product_id"))

    # File Type Of Science File (Foreign Key)
    file_type = Column(String, ForeignKey(f"{CONFIGURATION.mission_name}_file_type.short_name"))

    # File Level Of Science File (Foreign Key)
    file_level = Column(String, ForeignKey(f"{CONFIGURATION.mission_name}_file_level.short_name"))

    # Filename Of Science File
    filename = Column(String, unique=True)

    # File Version Of Science File
    file_version = Column(String)

    # File Extension Of Science File
    file_extension = Column(String)

    # File Path Of Science File
    file_path = Column(String)

    # File Size Of Science File
    file_size = Column(Integer)

    # File Modified Timestamp Of Science File
    file_modified_timestamp = Column(DateTime)

    # Is Public Of Science File
    is_public = Column(Boolean)

    parent = relationship("ScienceProductTable", back_populates="children")

    def __init__(
        self,
        science_product_id: int,
        file_type: str,
        file_level: str,
        filename: str,
        file_version: int,
        file_size: int,
        file_extension: str,
        file_path: str,
        file_modified_timestamp: datetime,
        is_public: bool,
    ) -> None:
        """
        Constructor for Science File Table
        """
        self.science_product_id = science_product_id
        self.file_type = file_type
        self.file_level = file_level
        self.filename = filename
        self.file_version = file_version
        self.file_size = file_size
        self.file_extension = file_extension
        self.file_path = file_path
        self.file_size = file_size
        self.file_modified_timestamp = file_modified_timestamp
        self.is_public = is_public

    def __repr__(self) -> str:
        return super().__repr__()


def return_class() -> type:
    """
    Return Class
    """
    return ScienceFileTable
