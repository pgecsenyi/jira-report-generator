class Config:

    def __init__(self, general_config, credentials_config, export_config):
        self._general = general_config
        self._credentials = credentials_config
        self._export = export_config

    @property
    def credentials(self):
        return self._credentials

    @property
    def export(self):
        return self._export

    @property
    def general(self):
        return self._general


class GeneralConfig:

    def __init__(self, server_url):
        self._server_url = server_url

    @property
    def server_url(self):
        return self._server_url


class CredentialsConfig:

    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username


class ExportConfig:

    def __init__(self, csv_format):
        self._csv_format = csv_format

    @property
    def csv_format(self):
        return self._csv_format


class CsvFormatConfig:

    def __init__(self, delimiter, quote_char, use_comma_as_decimal_separator):
        self._delimiter = delimiter
        self._quote_char = quote_char
        self._use_comma_as_decimal_separator = use_comma_as_decimal_separator

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def quote_char(self):
        return self._quote_char

    @property
    def use_comma_as_decimal_separator(self):
        return self._use_comma_as_decimal_separator
