from . import config


def load_config(new_config=None) -> config.CDFTrackerConfiguration:
    """
    Load configuration

    Args:
        config (Dict[str, Any], optional): Configuration. Defaults to None.

    Returns:
        config.CDFTrackerConfiguration: Configuration
    """

    return config.CDFTrackerConfiguration(new_config)
