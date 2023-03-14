from pathlib import Path
from typing import Callable

from hermes_core.util import util

file = Path("./hermes_MAG_l0_2022259-030002_v01.bin")


def track_file(path: Path, parser: Callable):
    """Track a file"""

    print(path)
    print(parser(path))


track_file(file, util.parse_science_filename)
