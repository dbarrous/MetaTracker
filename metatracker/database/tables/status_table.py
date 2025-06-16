# Status Table
# Schema:
#   status_id: int (primary key)
#   science_file_id: int (foreign key)
#   processing_status: str
#   processing_status_message: str
#   original_processing_timestamp: datetime
#   last_processing_timestamp: datetime
#   reprocessed_count: int
#   processing_time_length: int
#   origin_file_id: int (foreign key) (optional)


from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from metatracker import CONFIGURATION
from . import base_table as Base


status_origin_association = Table(
    f"{CONFIGURATION.mission_name}_status_origin_association",
    Base.Base.metadata,
    Column("status_id", Integer, ForeignKey(f"{CONFIGURATION.mission_name}_status.status_id"), primary_key=True),
    Column(
        "origin_file_id",
        Integer,
        ForeignKey(f"{CONFIGURATION.mission_name}_science_file.science_file_id"),
        primary_key=True,
    ),
)


class StatusTable(Base.Base):
    __tablename__ = f"{CONFIGURATION.mission_name}_status"

    # Primary Key
    status_id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    science_file_id = Column(
        Integer, ForeignKey(f"{CONFIGURATION.mission_name}_science_file.science_file_id"), nullable=False
    )

    # Many-to-many relationship to origin files
    origin_files = relationship(
        "ScienceFileTable",  # replace with actual class if it's named differently
        secondary=status_origin_association,
        backref="status_origins",
        lazy="joined",
    )

    # Processing Information
    processing_status = Column(String, nullable=False)
    processing_status_message = Column(String, nullable=True)
    original_processing_timestamp = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_processing_timestamp = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    reprocessed_count = Column(Integer, default=0)
    processing_time_length = Column(Integer, nullable=True)  # seconds

    def __init__(
        self,
        science_file_id: int,
        processing_status: String,
        processing_status_message: str = None,
        original_processing_timestamp: datetime = None,
        last_processing_timestamp: datetime = None,
        reprocessed_count: int = 0,
        processing_time_length: int = None,
        origin_files: list = None,
    ) -> None:
        self.science_file_id = science_file_id
        self.processing_status = processing_status
        self.processing_status_message = processing_status_message
        self.original_processing_timestamp = original_processing_timestamp or datetime.now(timezone.utc)
        self.last_processing_timestamp = last_processing_timestamp or datetime.now(timezone.utc)
        self.reprocessed_count = reprocessed_count
        self.processing_time_length = processing_time_length
        self.origin_files = origin_files

    def __repr__(self) -> str:
        return super().__repr__()


def return_class() -> type:
    return StatusTable
