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

try:
    with open("cdftracker/config.yaml") as config_file:
        config = yaml_safe_load(config_file)

        DB_HOST = os_environ("CDF_TRACKER_DB_HOST", "sqlite:///")

        MISSION_NAME = config["mission_name"]

        INSTRUMENTS = config["instruments"]

        INSTRUMENT_CONFIGURATIONS = config["instrument_configurations"]

        FILE_LEVELS = config["file_levels"]

        FILE_TYPES = config["file_types"]


except FileNotFoundError:
    log.exception("Config file not found. Exiting...")
    exit(1)

except KeyError as key_error:
    log.exception(f"Key {key_error} not found in config file. Exiting...")
    exit(1)
