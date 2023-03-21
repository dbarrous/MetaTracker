# CDFTracker


[![GitHub issues](https://img.shields.io/github/issues/HERMES-SOC/CDFTracker)](
[![Build status](https://img.shields.io/github/actions/workflow/status/HERMES-SOC/CDFTracker/main.yml?branch=main)](https://github.com/HERMES-SOC/CDFTracker/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/HERMES-SOC/CDFTracker/branch/main/graph/badge.svg)](https://codecov.io/gh/HERMES-SOC/CDFTracker)
[![Commit activity](https://img.shields.io/github/commit-activity/m/HERMES-SOC/CDFTracker)](https://img.shields.io/github/commit-activity/m/HERMES-SOC/CDFTracker)
[![License](https://img.shields.io/github/license/HERMES-SOC/CDFTracker)](https://img.shields.io/github/license/HERMES-SOC/CDFTracker)

This is a python package that helps keep track of both Raw Binary and CDF Files in a Relational Database.

- **Github repository**: <https://github.com/HERMES-SOC/CDFTracker/>

## Features
- Track both Raw Binary and CDF Files
- Supports multiple instrument configurations
- Support for multiple RDBMS via SQLAlchemy connection strings

## Requirements
- Python 3.8 or higher
- SQL Database (via connection string)
- [Make](https://www.gnu.org/software/make/manual/make.html) 
- [Poetry](https://github.com/python-poetry/poetry) (optional)

## Installation and Usage
To install the library and its dependencies, follow these steps:

1. Install with dependency manager of your choice:
    ```bash
    # Install with pip
    pip install git+https://github.com/HERMES-SOC/CDFTracker.git

    # Install with poetry
    poetry add git+https://github.com/HERMES-SOC/CDFTracker.git
    ```


2. Create both the engine and the session, with your RDBMS of choice connection string. For example, to create a session with a SQLite database, you can do the following:
    ```python
    from cdftracker.database import create_engine, create_session

    engine = create_engine("sqlite:///test.db")
    session = create_session(engine)
    ```

3. If this is your first time using the library, you will need to create the database tables. To do so, run the following command:
    ```python
    from cdftracker.database.tables import set_up_tables

    set_up_tables(engine, session)
    ```

4. Define a science file name parser function which parses the file Path object and returns the following information in a dictionary. This is the formart the dictionary outputted by the function should have:
    ```python
    # def science_file_name_parser():
    #    return {
      #      "instrument": str,
      #      "mode": str,
      #      "test": bool,
      #      "time": str,
      #      "level": str,
      #      "version": str,
      #      "descriptor": str,
    #    }
    ```
5. Now you can instantiate a `CDFTracker` object with the engine and science file parser function you defined:
    ```python
    from cdftracker import CDFTracker

    tracker = CDFTracker(engine, science_file_parser)
    tracker.track_file("path/to/file")
    ```
6. You can also `track` the file which adds the appropriate entries to the database. To do so, run the following command:
    ```python
    tracker.track("path/to/file")
    ```

## Database Schema
This is the database schema for the CDFTracker database. The database schema is defined in the `cdftracker.database.tables` module. 

## Contributing
### How to set-up Development Environment
This project makes use of [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments. Also included is a Make file to set-up your development environment. To set-up your development environment, follow these steps:

1. Clone the repository

    ```bash
    git clone https://github.com/HERMES-SOC/CDFTracker.git

    cd CDFTracker
    ```

2. Set-up your development environment

    ```bash
    make install
    ```


### How to run tests
This project uses [pytest](https://docs.pytest.org/en/stable/) to run tests and exports an HTML report of the code coverage. To run tests, follow these steps:

1. Inside the project directory, run the following command:

    ```bash
    make test
    ```


### How to run linter
This project uses black and ruff to lint the code. To run the linter, follow these steps:

1. Inside the project directory, run the following command:

    ```bash
    make check
    ```

## License
This project is licensed under the terms of the MIT license.


