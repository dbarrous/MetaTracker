# Set up logging
import logging
import os

# Set up basic config for logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Format Logging
color_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set Up Console Logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
log.addHandler(console_handler)


CDFTRACKER_CONFIG = {
    # Database Host Connection String
    "db_host": os.environ.get("CDFTRACKER_DB_HOST", "sqlite:///db.db"),
    # Name Of Mission for Tables
    "mission_name": "hermes",
    # Instruments
    "instruments": [
        {
            "instrument_id": 1,
            "full_name": "EEA",
            "short_name": "eea",
            "description": "Electron Electrostatic Analyzer (EEA)",
        },
        {
            "instrument_id": 2,
            "full_name": "NEMISIS",
            "short_name": "nemisis",
            "description": "Noise Eliminating Magnetometer Instrument in a Small Integrated System",
        },
        {
            "instrument_id": 3,
            "full_name": "SPANI-I",
            "short_name": "spani",
            "description": "Solar Probe Analyzer for Ions",
        },
        {
            "instrument_id": 4,
            "full_name": "MERIT",
            "short_name": "merit",
            "description": "Miniaturized Electron pRoton Telescope",
        },
    ],
    # Instrument Configurations
    # Should be a list of dictionaries
    # Each dictionary should have the following keys:
    # instrument_{i}_id: int
    # - Where i is the instrument number (starting at 1)
    # and the value is the instrument id
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
    # File Types
    "file_types": [
        {
            "full_name": "Raw Binary",
            "short_name": "raw",
            "description": "Raw Binary File",
        },
        {
            "full_name": "Common Data Format",
            "short_name": "cdf",
            "description": "Common Data Format File",
        },
    ],
    # File Levels
    "file_levels": [
        {
            "full_name": "Level 0",
            "short_name": "l0",
            "description": "Level 0 File",
        },
        {
            "full_name": "Level 1",
            "short_name": "l1",
            "description": "Level 1 File",
        },
        {
            "full_name": "Quick Look",
            "short_name": "ql",
            "description": "Quick Look File",
        },
    ],
}
