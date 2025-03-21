from pathlib import Path

from hermes_core.util import util

from metatracker import log
from metatracker.database import create_engine, create_session
from metatracker.database.tables import create_tables
from metatracker.database.tables.science_file_table import ScienceFileTable
from metatracker.database.tables.science_product_table import ScienceProductTable
from metatracker.tracker import tracker

TEST_DB_HOST = "sqlite://"
TEST_RANDOM_FILENAME = "./tests/test_files/ducks.txt"
TEST_SCIENCE_FILENAME = "./tests/test_files/hermes_MAG_l0_2022259-030002_v01.bin"
TEST_BAD_SCIENCE_FILENAME = "./tests/test_files/hermes_MAG_2l_2022259-030002_v01.bin"
TEST_NON_EXISTING_SCIENCE_FILENAME = "./hermes_MAG_l0_2022259-030002_v01.bop"
TEST_INSTRUMENTS = [
    {"instrument_id": 1, "full_name": "MAG", "short_name": "mag", "description": "Magnetometer"},
    {"instrument_id": 2, "full_name": "SIS", "short_name": "sis", "description": "Solar Wind Ion Spectrometer"},
]


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
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    file_name = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine, science_file_parser=science_file_parser)

    extension = test_tracker.parse_extension(file_name)

    assert extension == ".bin"

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
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
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

    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    test_bad_file = Path(TEST_NON_EXISTING_SCIENCE_FILENAME)

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    extension = test_tracker.parse_extension(test_bad_file)

    assert not test_tracker.is_valid_file_type(session=session, extension=extension)


def test_tracker_parse_filename() -> None:
    """
    Test Tracker parse filename
    """
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    file_name = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    filename = test_tracker.parse_filename(file_name)

    assert filename == "hermes_MAG_l0_2022259-030002_v01"

    file_name = Path(TEST_RANDOM_FILENAME)

    filename = test_tracker.parse_filename(file_name)

    assert filename == "ducks"


def test_tracker_parse_file() -> None:
    """
    Test Tracker parse file
    """
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
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

    file = test_tracker.parse_file(session, file_name)

    assert file is not None

    assert len(file.keys()) == 9

    test_tracker.add_to_science_file_table(session, file, 1)

    # Check that file is in database
    with session.begin() as sql_session:
        found_file = (
            sql_session.query(ScienceFileTable)
            .filter(ScienceFileTable.filename == "hermes_MAG_l0_2022259-030002_v01")
            .first()
        )

        assert found_file.filename == "hermes_MAG_l0_2022259-030002_v01"


def test_tracker_parse_science_file() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
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
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    test_file = Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument = test_tracker.parse_science_file_data(file=test_file)["instrument"]

    assert test_tracker.is_valid_instrument(session=session, instrument_short_name=instrument)

    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    test_file = Path(TEST_NON_EXISTING_SCIENCE_FILENAME)

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    try:
        instrument = test_tracker.parse_science_file_data(file=test_file)["instrument"]

    except ValueError as e:
        assert e is not None


def test_get_instruments() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instruments = test_tracker.get_instruments(session=session)

    assert instruments is not None

    assert len(instruments) == 4


def test_get_instrument_configurations() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument_configurations = test_tracker.get_instrument_configurations(session=session)

    assert instrument_configurations is not None

    assert len(instrument_configurations) == 4

    assert instrument_configurations[1] == ["eea"]

    log.info(instrument_configurations)


def test_get_instrument_by_id() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    Path(TEST_SCIENCE_FILENAME)

    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    instrument = test_tracker.get_instrument_by_id(session=session, instrument_id=1)

    assert instrument is not None

    assert instrument == "eea"


def test_map_instrument_list() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
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

    assert len(instrument_map) == 4


def test_track() -> None:
    # Create testfile with name hermes_MAG_l0_2022259-030002_v01.bin
    engine = create_engine(TEST_DB_HOST)

    session = create_session(engine)

    create_tables(engine=engine)

    # Science File Parser
    science_file_parser = util.parse_science_filename

    test_tracker = tracker.MetaTracker(engine=engine, science_file_parser=science_file_parser)

    test_tracker.track(file=Path(TEST_SCIENCE_FILENAME))

    # Test Non Existing File
    try:
        test_tracker.track(file=Path(TEST_NON_EXISTING_SCIENCE_FILENAME))

    except FileNotFoundError as e:
        assert e is not None

    # Check science file table and science product table were created
    with session.begin() as sql_session:
        files = sql_session.query(ScienceFileTable).all()
        assert files is not None
        products = sql_session.query(ScienceProductTable).all()
        assert products is not None

    assert test_tracker is not None

    # Test duplicate file tracking (should not raise error but update timestamp)
    test_tracker.track(file=Path(TEST_SCIENCE_FILENAME))

    # Test bad file type
    try:
        test_tracker.track(file=Path(TEST_RANDOM_FILENAME))

    except ValueError as e:
        assert e is not None

    # Test bad file name
    try:
        test_tracker.track(file=Path(TEST_BAD_SCIENCE_FILENAME))

    except ValueError as e:
        assert e is not None
