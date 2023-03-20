# CDFTracker

[![Release](https://img.shields.io/github/v/release/dbarrous/CDFTracker)](https://img.shields.io/github/v/release/dbarrous/CDFTracker)
[![Build status](https://img.shields.io/github/actions/workflow/status/dbarrous/CDFTracker/main.yml?branch=main)](https://github.com/dbarrous/CDFTracker/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/dbarrous/CDFTracker/branch/main/graph/badge.svg)](https://codecov.io/gh/dbarrous/CDFTracker)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dbarrous/CDFTracker)](https://img.shields.io/github/commit-activity/m/dbarrous/CDFTracker)
[![License](https://img.shields.io/github/license/dbarrous/CDFTracker)](https://img.shields.io/github/license/dbarrous/CDFTracker)

This is a python package that helps keep track of both Raw Binary and CDF Files in a Relational Database.

- **Github repository**: <https://github.com/dbarrous/CDFTracker/>

## How to set-up Development Environment
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

3. Code away!


## How to run tests
This project uses [pytest](https://docs.pytest.org/en/stable/) to run tests. To run tests, follow these steps:

1. Inside the project directory, run the following command:

    ```bash
    pytest 
    ```
