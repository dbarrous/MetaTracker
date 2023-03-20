# Set up logging
import logging
from os import getenv as os_environ

from yaml import safe_load as yaml_safe_load

# Set up basic config for logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Format Logging
color_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set Up Console Logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
log.addHandler(console_handler)

DEFAULT_CONFIG = {
    "db_host": "sqlite:///",
    "mission_name": "hermes",
    "instruments": [
        {
            "instrument_id": 1,
            "description": "Electron Electrostatic Analyzer (EEA)",
            "full_name": "EEA",
            "short_name": "eea",
        },
        {
            "instrument_id": 2,
            "description": "Noise Eliminating Magnetometer Instrument in a Small Integrated System",
            "full_name": "NEMISIS",
            "short_name": "nemisis",
        },
        {
            "instrument_id": 3,
            "description": "Solar Probe Analyzer for Ions",
            "full_name": "SPANI-I",
            "short_name": "spani",
        },
        {
            "instrument_id": 4,
            "description": "Miniaturized Electron pRoton Telescope",
            "full_name": "MERIT",
            "short_name": "merit",
        },
    ],
    "instrument_configurations": [
        {
            "instrument_configuration_id": 1,
            "instrument_1_id": 1,
            "instrument_2_id": None,
            "instrument_3_id": None,
            "instrument_4_id": None,
        },
        {
            "instrument_configuration_id": 2,
            "instrument_1_id": 2,
            "instrument_2_id": None,
            "instrument_3_id": None,
            "instrument_4_id": None,
        },
        {
            "instrument_configuration_id": 3,
            "instrument_1_id": 3,
            "instrument_2_id": None,
            "instrument_3_id": None,
            "instrument_4_id": None,
        },
        {
            "instrument_configuration_id": 4,
            "instrument_1_id": 4,
            "instrument_2_id": None,
            "instrument_3_id": None,
            "instrument_4_id": None,
        },
    ],
    "file_levels": [
        {"description": "Level 0 File", "full_name": "Level 0", "short_name": "l0"},
        {"description": "Level 1 File", "full_name": "Level 1", "short_name": "l1"},
        {"description": "Quick Look File", "full_name": "Quick Look", "short_name": "ql"},
    ],
    "file_types": [
        {"description": "Raw Binary File", "full_name": "Raw Binary", "short_name": "raw", "extension": ".bin"},
        {
            "description": "Common Data Format File",
            "full_name": "Common Data Format",
            "short_name": "cdf",
            "extension": ".cdf",
        },
    ],
}

# Define empty constants
DB_HOST = None
MISSION_NAME = None
INSTRUMENTS = None
INSTRUMENT_CONFIGURATIONS = None
FILE_LEVELS = None
FILE_TYPES = None
CONFIG = None

try:
    with open("cdftracker/config.yaml") as config_file:
        config = yaml_safe_load(config_file)

        DB_HOST = os_environ("CDF_TRACKER_DB_HOST", "sqlite:///")

        MISSION_NAME = config["mission_name"]

        INSTRUMENTS = config["instruments"]

        INSTRUMENT_CONFIGURATIONS = config["instrument_configurations"]

        FILE_LEVELS = config["file_levels"]

        FILE_TYPES = config["file_types"]

        # Create dicionary of all the config values
        CONFIG = {
            "db_host": DB_HOST,
            "mission_name": MISSION_NAME,
            "instruments": INSTRUMENTS,
            "instrument_configurations": INSTRUMENT_CONFIGURATIONS,
            "file_levels": FILE_LEVELS,
            "file_types": FILE_TYPES,
        }

        log.info('Loaded config file "cdftracker/config.yaml"')
        log.info(CONFIG)


except FileNotFoundError:
    log.exception("Config file not found. Exiting...")
    exit(1)

except KeyError as key_error:
    log.exception(f"Key {key_error} not found in config file. Exiting...")
    exit(1)


def load_config(config: dict = DEFAULT_CONFIG) -> dict:
    """Load config values from config dictionary"""

    DB_HOST = config["db_host"] if "db_host" in config else os_environ("CDF_TRACKER_DB_HOST", "sqlite:///")

    MISSION_NAME = config["mission_name"] if "mission_name" in config else DEFAULT_CONFIG["mission_name"]

    INSTRUMENTS = config["instruments"] if "instruments" in config else DEFAULT_CONFIG["instruments"]

    if "instrument_configurations" in config:
        INSTRUMENT_CONFIGURATIONS = config["instrument_configurations"]
    else:
        INSTRUMENT_CONFIGURATIONS = DEFAULT_CONFIG["instrument_configurations"]

    FILE_LEVELS = config["file_levels"] if "file_levels" in config else DEFAULT_CONFIG["file_levels"]

    FILE_TYPES = config["file_types"] if "file_types" in config else DEFAULT_CONFIG["file_types"]

    # Create dicionary of all the config values
    CONFIG = {
        "db_host": DB_HOST,
        "mission_name": MISSION_NAME,
        "instruments": INSTRUMENTS,
        "instrument_configurations": INSTRUMENT_CONFIGURATIONS,
        "file_levels": FILE_LEVELS,
        "file_types": FILE_TYPES,
    }

    return CONFIG
