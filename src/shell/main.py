import getpass
import pickle
import sys

from domain import exceptions
from domain.config import Config, CredentialsConfig
from domain.sprint import Sprint
from export.exporter_factory import create_exporter
from communication.jira_agent import JiraAgent
from shell.argument_parser import ArgumentParser
from shell.config_manager import ConfigManager


def run():
    try:
        argument_parser = ArgumentParser(sys.argv)
        if not argument_parser.parse():
            return

        config = load_configuration(argument_parser.config_file_path)
        sprint = load_data(argument_parser, config)

        if argument_parser.raw_data_target:
            save_data(sprint, argument_parser.raw_data_target)

        print('Exporting data...')
        export_result(
            sprint,
            argument_parser.output_file_path,
            config.export,
            argument_parser.export_format)

        print(F'Data exported successfully.')
    except exceptions.ArgumentParserException as exception:
        print(str(exception))
        argument_parser.print_help()
        sys.exit(1)
    except exceptions.ConfigManagerException as exception:
        print(str(exception))
        sys.exit(2)
    except exceptions.InvalidConfigException as exception:
        print(F'Configuration is invalid. {exception}')
        sys.exit(2)


def load_configuration(config_file_path):
    config_manager = ConfigManager(config_file_path)

    return config_manager.load()


def load_data(argument_parser, config):
    if argument_parser.raw_data_source:
        return load_data_from_file(argument_parser.raw_data_source)

    return download_data(config, argument_parser.jira_board_id, argument_parser.jira_sprint_name)


def load_data_from_file(file_path):
    print('Loading data from file...')
    with open(file_path, 'rb') as pkl_file:
        return pickle.load(pkl_file)


def download_data(config, jira_board_id, jira_sprint_name):
    config = verify_credentials(config)

    print('Connecting to JIRA...')
    agent = connect_to_jira(config)

    print('Retrieving sprint ID...')
    sprint_id = retreive_sprint_id(agent, jira_board_id, jira_sprint_name)

    print('Retrieving sprint info...')
    sprint_info = agent.retrieve_sprint_info(sprint_id)

    print('Downloading issues and work logs...')

    return Sprint(sprint_info, agent.download_work_log_of_sprint(sprint_id))


def save_data(sprint, file_path):
    print(F'Saving raw data to {file_path}...')
    with open(file_path, 'wb') as output:
        pickle.dump(sprint, output)


def verify_credentials(config):
    username = config.credentials.username
    password = config.credentials.password

    if username and password:
        return config

    (username, password) = ask_for_credentials(username, password)
    credentials_config = CredentialsConfig(username, password)
    config = Config(config.general, credentials_config, config.export)

    return config


def ask_for_credentials(username, password):
    if not username:
        username = input('Username: ')
        password = getpass.getpass()
    elif not password:
        password = getpass.getpass()

    return username, password


def connect_to_jira(config):
    agent = JiraAgent(config.general.server_url, config.credentials.username, config.credentials.password)
    agent.connect()

    return agent


def retreive_sprint_id(agent, board_id, sprint_name):
    sprint_id = agent.retrieve_sprint_id(board_id, sprint_name)
    if sprint_id == '':
        raise Exception(F'Cannot find JIRA sprint with name "{sprint_name}".')

    return sprint_id


def export_result(sprint_data, output_path, export_config, export_format):
    exporter = create_exporter(export_format, export_config)
    exporter.export(output_path, sprint_data)
