import configparser
import os

from domain.config import Config, CredentialsConfig, CsvFormatConfig, ExportConfig, GeneralConfig

SECTION_CREDENTIALS = 'credentials'
SECTION_CSV_FORMAT = 'csv_format'
SECTION_GENERAL = 'general'


class ConfigManager:

    def __init__(self, config_file_path):
        if config_file_path is None:
            raise Exception('config_file_path cannot be None.')

        self._config_file_path = config_file_path

    def load(self):
        if not os.path.exists(self._config_file_path):
            raise Exception('The configuration file ({0}) does not exist.'.format(self._config_file_path))

        config_parser = configparser.RawConfigParser()
        config_parser.read(self._config_file_path)

        return self._load_config_from_parser(config_parser)

    def save(self, config):
        config_parser = configparser.RawConfigParser()

        self._save_config_to_parser(config_parser, config)

        with open(self._config_file_path, 'w') as config_file:
            config_parser.write(config_file)

    def _load_config_from_parser(self, config_parser):
        general_config = self._load_general_config_from_parser(config_parser)
        credentials_config = self._load_credentials_config_from_parser(config_parser)
        export_config = self._load_export_config(config_parser)

        config = Config(general_config, credentials_config, export_config)

        return config

    def _load_general_config_from_parser(self, config_parser):
        server_url = config_parser.get(SECTION_GENERAL, 'server_url')
        general_config = GeneralConfig(server_url)

        return general_config

    def _load_credentials_config_from_parser(self, config_parser):
        username = config_parser.get(SECTION_CREDENTIALS, 'username')
        password = config_parser.get(SECTION_CREDENTIALS, 'password')
        credentials_config = CredentialsConfig(username, password)

        return credentials_config

    def _load_export_config(self, config_parser):
        csv_format = self._load_csv_format_config(config_parser)
        export_config = ExportConfig(csv_format)

        return export_config

    def _load_csv_format_config(self, config_parser):
        delimiter = config_parser.get(SECTION_CSV_FORMAT, 'delimiter')
        quote_char = config_parser.get(SECTION_CSV_FORMAT, 'quote_char')
        use_comma_as_decimal_separator = config_parser.getboolean(SECTION_CSV_FORMAT, 'use_comma_as_decimal_separator')
        csv_format_config = CsvFormatConfig(delimiter, quote_char, use_comma_as_decimal_separator)

        return csv_format_config

    def _save_config_to_parser(self, config_parser, config):
        config_parser.add_section(SECTION_GENERAL)
        config_parser.set(SECTION_GENERAL, 'server_url', config.general.server_url)

        config_parser.add_section(SECTION_CREDENTIALS)
        config_parser.set(SECTION_CREDENTIALS, 'username', config.credentials.username)
        config_parser.set(SECTION_CREDENTIALS, 'password', config.credentials.password)

        config_parser.add_section(SECTION_CSV_FORMAT)
        config_parser.set(SECTION_CSV_FORMAT, 'delimiter', config.export.csv_format.delimiter)
        config_parser.set(SECTION_CSV_FORMAT, 'quote_char', config.export.csv_format.quote_char)
        config_parser.setboolean(
            SECTION_CSV_FORMAT,
            'use_comma_as_decimal_separator',
            config.export.csv_format.use_comma_as_decimal_separator)
