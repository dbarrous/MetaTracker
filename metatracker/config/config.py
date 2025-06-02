"""
Module for configuration of the application.
"""

import os
from typing import Any, Dict, List

DEFAULT_CONFIG = {
    "db_host": "sqlite:///",
    "mission_name": "padre",
    "instruments": [
        {"instrument_id": 1, "description": "MeDDEA (MEDDEA)", "full_name": "MeDDEA", "short_name": "meddea"},
        {
            "instrument_id": 2,
            "description": "Solar HARd X-ray Polarimeter (SHARP)",
            "full_name": "Solar HARd X-ray Polarimeter",
            "short_name": "sharp",
        },
    ],
    "instrument_configurations": [
        {"instrument_configuration_id": 1, "instrument_1_id": 1, "instrument_2_id": None},
        {"instrument_configuration_id": 2, "instrument_1_id": 2, "instrument_2_id": None},
        {"instrument_configuration_id": 3, "instrument_1_id": 1, "instrument_2_id": 2},
    ],
    "file_levels": [
        {"description": "RAW File", "full_name": "RAW", "short_name": "raw"},
        {"description": "Level 0 File", "full_name": "Level 0", "short_name": "l0"},
        {"description": "Level 1 File", "full_name": "Level 1", "short_name": "l1"},
        {"description": "Quick Look File", "full_name": "Quick Look", "short_name": "ql"},
        {"description": "Level 2 File", "full_name": "Level 2", "short_name": "l2"},
        {"description": "Level 3 File", "full_name": "Level 3", "short_name": "l3"},
        {"description": "Level 4 File", "full_name": "Level 4", "short_name": "l4"},
    ],
    "file_types": [
        {"description": "Raw Binary File", "full_name": "Raw BINARY", "short_name": "bin", "extension": ".bin"},
        {"description": "Raw Dat File", "full_name": "Raw DAT", "short_name": "dat", "extension": ".dat"},
        {"description": "Raw IDX File", "full_name": "Raw IDX", "short_name": "idx", "extension": ".idx"},
        {
            "description": "Common Data Format File",
            "full_name": "Common Data Format",
            "short_name": "cdf",
            "extension": ".cdf",
        },
        {
            "description": "Flexible Image Transport System File",
            "full_name": "Flexible Image Transport System",
            "short_name": "fits",
            "extension": ".fits",
        },
    ],
}


class MetaTrackerConfiguration:
    db_host: str
    mission_name: str
    instruments: List[Dict[str, Any]]
    instrument_configurations: List[Dict[str, Any]]
    file_levels: List[Dict[str, Any]]
    file_types: List[Dict[str, Any]]

    def __init__(self, config: Dict[str, Any]) -> None:
        if config is None or config == {}:
            config = DEFAULT_CONFIG

        if "db_host" not in config:
            config["db_host"] = DEFAULT_CONFIG["db_host"]

        if "CDFTRACKER_DB_HOST" in os.environ:
            config["db_host"] = os.environ["CDFTRACKER_DB_HOST"]

        if "mission_name" not in config:
            config["mission_name"] = DEFAULT_CONFIG["mission_name"]

        if "instruments" not in config:
            config["instruments"] = DEFAULT_CONFIG["instruments"]

        if "instrument_configurations" not in config:
            config["instrument_configurations"] = DEFAULT_CONFIG["instrument_configurations"]

        if "file_levels" not in config:
            config["file_levels"] = DEFAULT_CONFIG["file_levels"]

        if "file_types" not in config:
            config["file_types"] = DEFAULT_CONFIG["file_types"]

        self.db_host = config["db_host"]
        self.mission_name = config["mission_name"]
        self.instruments = config["instruments"]
        self.instrument_configurations = config["instrument_configurations"]
        self.file_levels = config["file_levels"]
        self.file_types = config["file_types"]

    def __repr__(self) -> str:
        return (
            f"MetaTrackerConfiguration(db_host={self.db_host}, mission_name={self.mission_name},"
            f" instruments={self.instruments}, instrument_configurations={self.instrument_configurations},"
            f" file_levels={self.file_levels}, file_types={self.file_types})"
        )

    def __str__(self) -> str:
        return self.__repr__()
