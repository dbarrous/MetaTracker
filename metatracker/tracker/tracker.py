from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError, IntegrityError


from metatracker import log
from metatracker.database import check_connection, create_session
from metatracker.database.tables.file_level_table import FileLevelTable
from metatracker.database.tables.file_type_table import FileTypeTable
from metatracker.database.tables.instrument_configuration_table import InstrumentConfigurationTable
from metatracker.database.tables.instrument_table import InstrumentTable
from metatracker.database.tables.science_file_table import ScienceFileTable
from metatracker.database.tables.science_product_table import ScienceProductTable
from metatracker.database.tables.status_table import StatusTable

db_retry = retry(
    reraise=True,
    stop=stop_after_attempt(5),  # Try up to 5 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # 2s, 4s, 8s, 10s, 10s
    retry=(retry_if_exception_type(OperationalError) | retry_if_exception_type(IntegrityError)),
)


class MetaTracker:
    def __init__(self, engine, science_file_parser: Callable):
        self.engine = engine

        try:
            check_connection(self.engine)
        except Exception:
            raise ConnectionError("Database connection is not valid") from None

        self.science_file_parser = science_file_parser

    def track(
        self, file: Path, s3_key: str, s3_bucket: str, science_product_id: int = None, status: dict = None
    ) -> tuple:
        """Track a file"""
        if not self.is_file_real(file):
            log.debug("File does not exist")
            raise FileNotFoundError("File does not exist")
        session = create_session(self.engine)

        parsed_file = self.parse_file(session, file, s3_key, s3_bucket)
        parsed_science_product = self.parse_science_product(session, file)

        # Check if science_product_id is provided
        if science_product_id is None:
            science_product_id = self.add_to_science_product_table(
                session=session, parsed_science_product=parsed_science_product
            )
            log.debug("Added to Science Product Table")
        else:
            log.debug(f"Using existing science_product_id: {science_product_id}")

        # Add to science file table
        log.debug("Added to Science Product Table")
        science_file_id = self.add_to_science_file_table(
            session=session, parsed_file=parsed_file, science_product_id=science_product_id
        )
        log.debug("Added to Science File Table")

        if status:
            # Add to status table if status is provided
            log.debug("Added to Status Table")
            self.add_to_status_table(
                session=session,
                science_file_id=science_file_id,
                processing_status=status.get("processing_status"),
                processing_status_message=status.get("processing_status_message"),
                processing_time_length=status.get("processing_time_length"),
                origin_file_ids=status.get("origin_file_ids", None),
            )

        return science_file_id, science_product_id

    @db_retry
    def add_to_science_file_table(self, session: type, parsed_file: dict, science_product_id: int) -> int:
        """Add a file to the file table"""

        with session.begin() as sql_session:
            if not parsed_file:
                log.debug("File is not valid")
                return

            # 1. Check for existing file by UNIQUE constraint (filename)
            file = (
                sql_session.query(ScienceFileTable)
                .filter(ScienceFileTable.filename == parsed_file["filename"])
                .first()
            )

            if file:
                # Optionally update fields if needed (for now just return the id)
                log.debug(f"File already exists in Science File Table with id: {file.science_file_id}")
                return file.science_file_id

            # 2. If not found, insert new
            file = ScienceFileTable(
                science_product_id=science_product_id,
                file_type=parsed_file["file_type"],
                file_level=parsed_file["file_level"],
                filename=parsed_file["filename"],
                file_version=parsed_file["file_version"],
                file_size=parsed_file["file_size"],
                s3_key=parsed_file["s3_key"],
                s3_bucket=parsed_file["s3_bucket"],
                file_extension=parsed_file["file_extension"],
                file_path=parsed_file["file_path"],
                file_modified_timestamp=parsed_file["file_modified_timestamp"],
                is_public=parsed_file["is_public"],
            )
            sql_session.add(file)
            sql_session.flush()
            science_file_id = file.science_file_id
            log.debug(f"Added file to Science File Table with id: {science_file_id}")
            return science_file_id

    @db_retry
    def add_to_science_product_table(self, session: type, parsed_science_product: dict):
        sess = session()

        # Check if science product exists with same instrument configuration id, mode, and reference timestamp
        science_product = (
            sess.query(ScienceProductTable)
            .filter(
                ScienceProductTable.instrument_configuration_id
                == parsed_science_product["instrument_configuration_id"],
                ScienceProductTable.mode == parsed_science_product["mode"],
                ScienceProductTable.reference_timestamp == parsed_science_product["reference_timestamp"],
            )
            .first()
        )

        # If science product exists, return science product id
        if science_product:
            return science_product.science_product_id

        # If science product doesn't exist, add it to the database
        science_product = ScienceProductTable(
            instrument_configuration_id=parsed_science_product["instrument_configuration_id"],
            mode=parsed_science_product["mode"],
            reference_timestamp=parsed_science_product["reference_timestamp"],
        )
        sess.add(science_product)
        sess.commit()

        # return science product id that was just added
        return science_product.science_product_id

    @db_retry
    def add_to_status_table(
        self,
        session: type,
        science_file_id: int,
        processing_status: str,
        processing_status_message: str = None,
        processing_time_length: int = None,
        origin_file_ids: list[int] = None,
    ) -> int:
        """Add or update a status entry for a science file in the status table."""

        with session.begin() as sql_session:
            # Validate and fetch origin files if provided
            origin_files = []
            if origin_file_ids is not None:
                if not isinstance(origin_file_ids, list) or not all(isinstance(i, int) for i in origin_file_ids):
                    raise ValueError("origin_file_ids must be a list of integers or None")
                origin_files = (
                    sql_session.query(ScienceFileTable)
                    .filter(ScienceFileTable.science_file_id.in_(origin_file_ids))
                    .all()
                )

            # Check if status already exists
            status = sql_session.query(StatusTable).filter(StatusTable.science_file_id == science_file_id).first()

            if status:
                # Update fields
                status.processing_status = processing_status
                status.processing_status_message = processing_status_message
                status.last_processing_timestamp = datetime.now(timezone.utc)
                status.reprocessed_count += 1
                status.processing_time_length = processing_time_length

                # Extend existing origin_files without duplicates
                if origin_files:
                    existing_ids = {f.science_file_id for f in status.origin_files}
                    new_files = [f for f in origin_files if f.science_file_id not in existing_ids]
                    status.origin_files.extend(new_files)

            else:
                # Create new entry
                status = StatusTable(
                    science_file_id=science_file_id,
                    processing_status=processing_status,
                    processing_status_message=processing_status_message,
                    processing_time_length=processing_time_length,
                    origin_files=origin_files,
                )
                sql_session.add(status)

            sql_session.flush()
            return status.status_id

    @staticmethod
    def get_file_size(file: Path) -> int:
        """Get file size"""
        return file.stat().st_size

    @staticmethod
    def get_file_modified_timestamp(file: Path) -> datetime:
        """Get file modified time"""

        return datetime.fromtimestamp(file.stat().st_mtime)

    @staticmethod
    def is_file_real(file: Path) -> bool:
        """Check if file exists"""
        return file.is_file()

    def is_valid_file_product(self, file: Path) -> bool:
        """Check if a file is a valid product"""

        return self.is_valid_file_type(extension=self.parse_extension(file))

    def parse_science_file_data(self, file: Path) -> dict:
        """Parse a science file"""

        return self.science_file_parser(file)

    def parse_file(self, session, file: Path, s3_key: str, s3_bucket: str) -> dict:
        """Parse a file"""

        if self.is_file_real(file):
            extension = self.parse_extension(file)
            if not self.is_valid_file_type(session=session, extension=extension):
                log.debug("File type is not valid")
                return {}

            science_file_data = self.parse_science_file_data(file)

            if not self.is_valid_file_level(session=session, file_level=science_file_data["level"]):
                log.debug("File level is not valid")
                return {}

            return {
                "file_path": self.parse_absolute_path(file),
                "s3_key": s3_key,
                "s3_bucket": s3_bucket,
                "filename": self.parse_filename(file),
                "file_extension": self.parse_extension(file),
                "file_size": self.get_file_size(file),
                "file_modified_timestamp": self.get_file_modified_timestamp(file),
                "file_level": science_file_data["level"],
                "file_type": self.get_file_type(session=session, extension=extension),
                "file_version": science_file_data["version"],
                "is_public": True,
            }

        return {}

    def parse_science_product(self, session, file: Path) -> dict:
        if self.is_file_real(file):
            science_product_data = self.parse_science_file_data(file)

            if not self.is_valid_timestamp(science_product_data["time"]):
                log.debug("Timestamp is not valid")
                return {}

            # Check if value is already a datetime object
            if isinstance(science_product_data["time"].value, datetime):
                reference_timestamp = science_product_data["time"].value
            else:
                reference_timestamp = datetime.strptime(science_product_data["time"].value, "%Y-%m-%dT%H:%M:%S.%f")

            if not self.is_valid_instrument(session=session, instrument_short_name=science_product_data["instrument"]):
                log.debug("Instrument is not valid")
                return {}

            config = self.get_instrument_configurations(session=session)

            if [science_product_data["instrument"]] not in config.values():
                log.debug("Instrument configuration is not valid")
                return {}

            # return Key with matching list values
            instrument_config_id = [k for k, v in config.items() if science_product_data["instrument"] in v][0]
            if not instrument_config_id:
                raise ValueError(f"Instrument configuration id not found {science_product_data}")

            return {
                "instrument_configuration_id": instrument_config_id,
                "reference_timestamp": reference_timestamp,
                "mode": science_product_data["mode"],
            }

    @staticmethod
    def is_valid_timestamp(timestamp: datetime) -> bool:
        """Check if a timestamp is valid"""

        return timestamp is not None

    @staticmethod
    def is_valid_instrument(session: type, instrument_short_name: str) -> bool:
        """Check if an instrument is valid"""

        with session.begin() as sql_session:
            instruments = sql_session.query(InstrumentTable).all()
            valid_instrument_short_names = [instrument.short_name for instrument in instruments]

            return instrument_short_name in valid_instrument_short_names

    @staticmethod
    def get_file_type(session: type, extension: str):
        """Get the file type of a file"""

        with session.begin() as sql_session:
            file_type = sql_session.query(FileTypeTable).filter(FileTypeTable.extension == extension).first()

            return file_type.short_name

    @staticmethod
    def is_valid_file_type(session: type, extension: str):
        """Check if a file extension is valid file type in the database"""

        with session.begin() as sql_session:
            file_types = sql_session.query(FileTypeTable).all()
            valid_extensions = [file_type.extension for file_type in file_types]

            return extension in valid_extensions

    @staticmethod
    def is_valid_file_level(session: type, file_level: str):
        """Check if a file level is valid file level in the database"""

        with session.begin() as sql_session:
            file_levels = sql_session.query(FileLevelTable).all()
            valid_file_levels = [file_level.short_name for file_level in file_levels]

            return file_level in valid_file_levels

    @staticmethod
    def parse_extension(file: Path) -> str:
        """Parse the extension of a file"""

        return file.suffix.lower()

    @staticmethod
    def parse_filename(file: Path) -> str:
        """Parse the filename of a file"""

        return file.stem

    @staticmethod
    def parse_absolute_path(file: Path) -> str:
        """Parse the path of a file"""

        return str(file.absolute())

    @staticmethod
    def get_instruments(session: type) -> list:
        """Get all instruments from the database
        {instrument_id: "instrument_short_name"}
        """

        with session.begin() as sql_session:
            instruments = sql_session.query(InstrumentTable).all()
            instruments = {instrument.instrument_id: instrument.short_name for instrument in instruments}

            return instruments

    def get_instrument_configurations(self, session: type) -> dict:
        """Get all configurations from the database
        {configuration_id: [instrument_1_id, instrument_2_id, ...]}
        """

        with session.begin() as sql_session:
            # Get amount of instruments from InstrumentTable
            instruments = self.get_instruments(session)
            amount_of_instruments = len(instruments)
            configurations = sql_session.query(InstrumentConfigurationTable).all()

            instrument_configurations = {}
            for config in configurations:
                # For the amount of instruments
                instruments = []
                for i in range(amount_of_instruments):
                    attribute = getattr(config, "instrument_" + str(i + 1) + "_id")
                    if attribute is not None:
                        attribute = self.get_instrument_by_id(session, int(attribute))
                        instruments.append(attribute)

                instruments.sort()
                instrument_configurations[config.instrument_configuration_id] = instruments

            return instrument_configurations

    def get_instrument_by_id(self, session, instrument_id: int) -> str:
        """Get instrument by id"""

        with session.begin():
            instruments = self.get_instruments(session)
            return instruments[instrument_id]

    def map_instrument_list(self, session: type, instrument_list: list) -> list:
        """Map an instrument list of id to a list of instrument shortnames"""

        with session.begin():
            return [self.get_instrument_by_id(session, instrument_id) for instrument_id in instrument_list]

    def get_failed_files(self) -> list:
        """Get all files with status 'FAILED'."""
        session = create_session(self.engine)

        # Query the StatusTable for records with 'FAILED' processing status
        failed_files_query = (
            session.query(ScienceFileTable.s3_key, ScienceFileTable.s3_bucket)
            .join(StatusTable, StatusTable.science_file_id == ScienceFileTable.science_file_id)
            .filter(StatusTable.processing_status == "FAILED")
        )

        # Fetch the results and return them as a list of tuples (s3_key, s3_bucket)
        failed_files = failed_files_query.all()

        return failed_files
