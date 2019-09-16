from domain.exceptions import InvalidConfigException
from domain.export_formats import CSV_FORMAT, SIMPLE_HTML_FORMAT
from export.csv.csv_exporter import CsvExporter
from export.simple_html.simple_html_exporter import SimpleHtmlExporter


def create_exporter(exporter_type, config):
    if exporter_type == CSV_FORMAT:
        return CsvExporter(config.csv_format)
    if exporter_type == SIMPLE_HTML_FORMAT:
        return SimpleHtmlExporter()

    raise InvalidConfigException('No such exporter.')
