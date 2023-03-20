import logging

from cdftracker import load_config, log


def test_log() -> None:
    """
    Test log
    """

    # Check if log is created
    assert log is not None

    # Check if log is a logger
    assert isinstance(log, logging.Logger)

    # Check if log has a handler
    assert len(log.handlers) > 0


def test_load_config() -> None:
    """
    Test load_config
    """

    default_config = load_config()

    log.info(default_config)

    assert default_config is not None

    assert len(default_config.keys()) == 6

    new_value_config = load_config({"mission_name": "test"})

    assert new_value_config is not None

    assert len(new_value_config.keys()) == 6

    assert new_value_config["mission_name"] == "test"
