import os
from datetime import datetime, timezone
from pathlib import Path

# Set SWXSOC_MISSION environment variable
os.environ["SWXSOC_MISSION"] = "padre"

from swxsoc.util import util

from metatracker import log
from metatracker.database import create_engine, create_session
from metatracker.database.tables import create_tables
from metatracker.database.tables.science_file_table import ScienceFileTable
from metatracker.database.tables.science_product_table import ScienceProductTable
from metatracker.database.tables.status_table import StatusTable
from metatracker.tracker import tracker

TEST_DB_HOST = "sqlite://"
TEST_RANDOM_FILENAME = "./tests/test_files/ducks.txt"
TEST_SCIENCE_FILENAME = "./tests/test_files/padreMDA0_250403185914.dat"
TEST_SCIENCE_FILENAME = "./tests/test_files/padreMDA0_250403185914.dat"
TEST_BAD_SCIENCE_FILENAME = "./tests/test_files/hermes_NEM_2l_2022259-030002_v01.bin"
TEST_NON_EXISTING_SCIENCE_FILENAME = "./hermes_NEM_l0_2022259-030002_v01.bop"


def test_tracker() -> None:
    """
    Test Tracker
    """
    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    assert test_tracker is not None

    # trunk-ignore(mypy/assignment)
    engine = "not_an_engine"

    # Science File Parser
    science_file_parser = util.parse_science_filename

    try:
        test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)
    except Exception as e:
        assert isinstance(e, ConnectionError)


def test_tracker_parse_extension() -> None:
    """
    Test Tracker parse extension
    """
    # Create testfile with name padreMDA0_250403185914.dat
    file_name = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine, science_file_parser=science_file_parser)

    extension = test_tracker.parse_extension(file_name)

    assert extension == ".dat"

    file_name = Path(TEST_RANDOM_FILENAME)

    extension = test_tracker.parse_extension(file_name)

    assert extension == ".txt"

    file_name = Path(TEST_NON_EXISTING_SCIENCE_FILENAME)

    extension = test_tracker.parse_extension(file_name)

    assert extension == ".bop"


def test_tracker_is_valid_file_type() -> None:
    """
    Test Tracker is valid file type
    """
    # Create testfile with name padreMDA0_250403185914.dat
    test_good_file = Path(TEST_SCIENCE_FILENAME)

    # Create engine and session
    engine = create_engine(TEST_DB_HOST)
    session = create_session(engine)

    # Set up tables
    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    extension = test_tracker.parse_extension(test_good_file)

    assert test_tracker.is_valid_file_type(session=session, extension=extension)

    # Create testfile with name padreMDA0_250403185914.dat
    test_bad_file = Path(TEST_NON_EXISTING_SCIENCE_FILENAME)

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    extension = test_tracker.parse_extension(test_bad_file)

    assert not test_tracker.is_valid_file_type(session=session, extension=extension)


def test_tracker_parse_filename() -> None:
    """
    Test Tracker parse filename
    """
    # Create testfile with name padreMDA0_250403185914.dat
    file_name = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    filename = test_tracker.parse_filename(file_name)

    assert filename == "padreMDA0_250403185914"

    file_name = Path(TEST_RANDOM_FILENAME)

    filename = test_tracker.parse_filename(file_name)

    assert filename == "ducks"


def test_tracker_parse_file() -> None:
    """
    Test Tracker parse file
    """
    # Create testfile with name padreMDA0_250403185914.dat
    file_name = Path(TEST_SCIENCE_FILENAME)

    # Create file TEST_SCIENCE_FILENAME
    with open(TEST_SCIENCE_FILENAME, "w") as f:
        f.write("Test")

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)
    # Science File Parser

    create_tables(engine=engine)

    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    s3_key = "s3://padre/test_file/padreMDA0_250403185914.dat"
    s3_bucket = "padre"

    file = test_tracker.parse_file(session, file_name, s3_key, s3_bucket)

    assert file is not None

    assert len(file.keys()) == 11

    test_tracker.add_to_science_file_table(session, file, 1)

    # Check that file is in database
    with session.begin() as sql_session:
        found_file = (
            sql_session.query(ScienceFileTable).filter(ScienceFileTable.filename == "padreMDA0_250403185914").first()
        )

        assert found_file.filename == "padreMDA0_250403185914"
        assert found_file.s3_key == s3_key
        assert found_file.s3_bucket == s3_bucket


def test_add_to_status_table() -> None:
    """
    Test add_to_status_table function
    """
    # Setup: Create a test database and session
    engine = create_engine(TEST_DB_HOST)
    session = create_session(engine)
    create_tables(engine=engine)

    # Create a test science file entry in the database
    science_file_id = 1
    with session.begin() as sql_session:
        science_file = ScienceFileTable(
            science_product_id=1,
            file_type="dat",
            file_level="L1",
            filename="test_file",
            file_version="1.0",
            file_size=1024,
            s3_key="s3://test_bucket/test_file.dat",
            s3_bucket="test_bucket",
            file_extension=".dat",
            file_path="/tmp/test_file.dat",
            file_modified_timestamp=datetime.now(timezone.utc),
            is_public=True,
        )
        sql_session.add(science_file)
        sql_session.flush()
        science_file_id = science_file.science_file_id

    # Initialize MetaTracker instance
    science_file_parser = util.parse_science_filename
    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    # Test: Add a new status entry
    processing_status = "SUCCESS"
    processing_status_message = "Processing started"
    origin_file_id = None

    status_id = test_tracker.add_to_status_table(
        session=session,
        science_file_id=science_file_id,
        processing_status=processing_status,
        processing_status_message=processing_status_message,
        origin_file_id=origin_file_id,
    )

    assert status_id is not None

    # Verify: Check that the status entry was added to the database
    with session.begin() as sql_session:
        status_entry = sql_session.query(StatusTable).filter(StatusTable.science_file_id == science_file_id).first()

        assert status_entry is not None
        assert status_entry.science_file_id == science_file_id
        assert status_entry.processing_status == processing_status
        assert status_entry.processing_status_message == processing_status_message
        assert status_entry.reprocessed_count == 0  # Initial value
        assert status_entry.origin_file_id == origin_file_id

    # Test: Update an existing status entry
    updated_processing_status = "FAILURE"
    updated_processing_status_message = "Processing failed"
    updated_processing_time_length = 120  # seconds

    updated_status_id = test_tracker.add_to_status_table(
        session=session,
        science_file_id=science_file_id,
        processing_status=updated_processing_status,
        processing_status_message=updated_processing_status_message,
        processing_time_length=updated_processing_time_length,
        origin_file_id=origin_file_id,
    )

    assert updated_status_id == status_id  # Ensure the same entry was updated

    # Verify: Check that the status entry was updated in the database
    with session.begin() as sql_session:
        updated_status_entry = (
            sql_session.query(StatusTable).filter(StatusTable.science_file_id == science_file_id).first()
        )

        assert updated_status_entry is not None
        assert updated_status_entry.processing_status == updated_processing_status
        assert updated_status_entry.processing_status_message == updated_processing_status_message
        assert updated_status_entry.reprocessed_count == 1  # Incremented value
        assert updated_status_entry.processing_time_length == updated_processing_time_length


def test_tracker_parse_science_file() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    test_file = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    science_file = test_tracker.parse_science_file_data(file=test_file)

    assert science_file is not None

    assert all(elem in science_file for elem in ["mode", "instrument", "time"])

    log.info(test_tracker.parse_science_file_data(file=test_file))


def test_track_is_valid_instrument() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    test_file = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument = test_tracker.parse_science_file_data(file=test_file)["instrument"]

    assert test_tracker.is_valid_instrument(session=session, instrument_short_name=instrument)

    # Create testfile with name padreMDA0_250403185914.dat
    test_file = Path(TEST_NON_EXISTING_SCIENCE_FILENAME)

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    try:
        instrument = test_tracker.parse_science_file_data(file=test_file)["instrument"]

    except ValueError as e:
        assert e is not None


def test_get_instruments() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instruments = test_tracker.get_instruments(session=session)

    assert instruments is not None

    assert len(instruments) == 2


def test_get_instrument_configurations() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument_configurations = test_tracker.get_instrument_configurations(session=session)

    assert instrument_configurations is not None

    assert len(instrument_configurations) == 3

    assert instrument_configurations[1] == ["meddea"]

    log.info(instrument_configurations)


def test_get_instrument_by_id() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument = test_tracker.get_instrument_by_id(session=session, instrument_id=1)

    assert instrument is not None

    assert instrument == "meddea"


def test_map_instrument_list() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument_list = test_tracker.get_instruments(session=session)

    instrument_map = test_tracker.map_instrument_list(session=session, instrument_list=instrument_list)

    assert instrument_map is not None

    assert len(instrument_map) == 2


def test_track() -> None:
    # Create testfile with name padreMDA0_250403185914.dat
    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)
    s3_key = "s3://padre/test_file/padreMDA0_250403185914.dat"
    s3_bucket = "padre"
    file_path = Path(TEST_SCIENCE_FILENAME)

    # Create file TEST_SCIENCE_FILENAME
    with open(TEST_SCIENCE_FILENAME, "w") as f:
        f.write("Test")

    # Define a test status
    test_status = {
        "processing_status": "SUCCESS",
        "processing_status_message": "Initial status",
        "processing_time_length": 60,
        "origin_file_id": None,
    }

    test_tracker.track(file=file_path, s3_key=s3_key, s3_bucket=s3_bucket, status=test_status)

    # Test Non Existing File
    try:
        test_tracker.track(file=Path(TEST_NON_EXISTING_SCIENCE_FILENAME), s3_key=s3_key, s3_bucket=s3_bucket)

    except FileNotFoundError as e:
        assert e is not None

    # Check science file table and science product table were created
    with session.begin() as sql_session:
        files = sql_session.query(ScienceFileTable).all()
        assert files is not None
        products = sql_session.query(ScienceProductTable).all()
        assert products is not None

        # Verify status entry
        status_entry = sql_session.query(StatusTable).first()
        assert status_entry is not None
        assert status_entry.processing_status == test_status["processing_status"]
        assert status_entry.processing_status_message == test_status["processing_status_message"]
        assert status_entry.processing_time_length == test_status["processing_time_length"]
        assert status_entry.origin_file_id == test_status["origin_file_id"]

    assert test_tracker is not None

    # Test duplicate file tracking (should not raise error but update timestamp)
    test_tracker.track(file=Path(TEST_SCIENCE_FILENAME), s3_key=s3_key, s3_bucket=s3_bucket)

    # Test bad file type
    try:
        test_tracker.track(file=Path(TEST_RANDOM_FILENAME), s3_key=s3_key, s3_bucket=s3_bucket)

    except ValueError as e:
        assert e is not None

    # Test bad file name
    try:
        test_tracker.track(file=Path(TEST_BAD_SCIENCE_FILENAME), s3_key=s3_key, s3_bucket=s3_bucket)

    except ValueError as e:
        assert e is not None
