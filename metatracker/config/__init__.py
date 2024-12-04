from . import config


def load_config(new_config=None) -> config.MetaTrackerConfiguration:
    """
    Load configuration

    Args:
        config (Dict[str, Any], optional): Configuration. Defaults to None.

    Returns:
        config.MetaTrackerConfiguration: Configuration
    """

    return config.MetaTrackerConfiguration(new_config)
