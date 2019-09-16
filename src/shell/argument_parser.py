import getopt

from domain import exceptions
from domain.export_formats import CSV_FORMAT, SIMPLE_HTML_FORMAT


class ArgumentParser:

    def __init__(self, arguments):
        self._application_name = ''
        self._arguments = arguments
        self._config_file_path = None
        self._export_format = CSV_FORMAT
        self._jira_board_id = None
        self._jira_sprint_name = None
        self._output_file_path = None
        self._raw_data_source = ''
        self._raw_data_target = ''

    @property
    def config_file_path(self):
        return self._config_file_path

    @property
    def export_format(self):
        return self._export_format

    @property
    def jira_board_id(self):
        return self._jira_board_id

    @property
    def jira_sprint_name(self):
        return self._jira_sprint_name

    @property
    def output_file_path(self):
        return self._output_file_path

    @property
    def raw_data_source(self):
        return self._raw_data_source

    @property
    def raw_data_target(self):
        return self._raw_data_target

    def parse(self):
        self._application_name, parameters = self._arguments[0], self._arguments[1:]

        try:
            shortopts = 'b:ce::hl:o:s:x:'
            longopts = [
                'board-id=',
                'config=',
                'export-format=',
                'help',
                'load-from=',
                'output=',
                'sprint-name=',
                'save-to=']
            opts, _ = getopt.getopt(parameters, shortopts, longopts)
        except getopt.GetoptError as ex:
            raise exceptions.ArgumentParserException(ex)

        for opt, arg in opts:
            if opt in ('-b', '--board-id'):
                self._jira_board_id = arg
            if opt in ('-c', '--config'):
                self._config_file_path = arg
            if opt in ('-e', '--export-format'):
                self._export_format = arg
            elif opt in ('-h', '--help'):
                self.print_help()
                return False
            if opt in ('-l', '--load-from'):
                self._raw_data_source = arg
            if opt in ('-o', '--output'):
                self._output_file_path = arg
            if opt in ('-s', '--sprint-name'):
                self._jira_sprint_name = arg
            if opt in ('-x', '--save-to'):
                self._raw_data_target = arg

        self._validate_arguments()

        return True

    def print_help(self):
        print('python {0} <options>'.format(self._application_name))
        print('')
        print('  -b, --board-id        The ID of the JIRA board.')
        print('  -c, --config          The path of the configuration file.')
        print('  -e, --export-format   Export format which can be either "CSV" or "SIMPLE_HTML".')
        print('  -h, --help            Print this help and exit.')
        print('  -l, --load-from       Load raw data from file instead of downloading it.')
        print('  -o, --output          The path of the output file.')
        print('  -s, --sprint-name     The name of the JIRA sprint.')
        print('  -x, --save-to         Save downloaded raw data.')
        print('')

    def _validate_arguments(self):
        if self._config_file_path == '':
            raise exceptions.ArgumentParserException('Configuration file path must be provided.')
        if self._export_format != CSV_FORMAT and self._export_format != SIMPLE_HTML_FORMAT:
            raise exceptions.ArgumentParserException('Invalid export format.')
