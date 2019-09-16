# JIRA Report Generator

Generates work time reports based on the work logs available in JIRA. It can download the data from JIRA or deserialize it from a Pickle file saved earlier.

## Installation

In order to install the application you will need the Python interpreter, specifically version 3.7 or later. You will also have to install _pip_ and _Pipenv_. The latter can be installed by issuing the following command.

    python -m pip install pipenv

Having all the basic requirements available this software can be installed with the following command executed from the `src` directory.

    python -m pipenv install

## Usage

Use the following command to execute the application.

    python -m pipenv run python main.py <arguments>

The list of available arguments can be found below.

  * `-b`, `--board-id`: The ID of the JIRA board to read data from. Ignored when the `-l` switch is provided.
  * `-c`, `--config`: The path of the configuration file.
  * `-e`, `--export-format`: The application can export results in CSV or HTML format. The latter is more detailed. The value of this argument can either be `CSV` or `SIMPLE_HTML`.
  * `-h`, `--help`: Display help and exit.
  * `-l`, `--load-from`: The path of a serialized Pickle file to load JIRA data from.
  * `-o`, `--output`: The path of the exported result.
  * `-s`, `--sprint-name`: The name of the sprint to get the data for. Ignored when the `-l` switch is provided.
  * `-x`, `--save-to`: When provided, the application will save Pickle-serialized object data to the given path after downloading data from JIRA.

## Development

Install developer dependencies first by running the following command.

    python -m pipenv install --dev

Linting can be done the following way.

    python -m pipenv run python lint_runner.py

_Visual Studio Code_ can be used to debug the application, but first you will need to create the `launch.json` and `settings.json` files under the `.vscode` folder based on the sample files provided.

### Environment

  * Windows 10
  * Python 3.7
