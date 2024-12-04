# Set up logging
import logging

from metatracker.config import load_config

# Set up basic config for logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Format Logging
color_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set Up Console Logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
log.addHandler(console_handler)


CONFIGURATION = load_config()


def get_config():
    """
    Get config
    """
    return CONFIGURATION


def set_config(config: dict) -> None:
    """
    Set config
    """
    global CONFIGURATION

    CONFIGURATION = load_config(config)
