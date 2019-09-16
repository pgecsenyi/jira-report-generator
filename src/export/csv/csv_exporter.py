import csv

from export.csv.spent_time_calculation import summarize_spent_time_by_author
from export.exporter import Exporter


class CsvExporter(Exporter):

    def __init__(self, config):
        self._config = config

    def export(self, filename, sprint):
        aggregated_work_log, authors = summarize_spent_time_by_author(sprint)

        with open(filename, 'wt') as csv_file:
            csv_writer = self._open_csv_writer(csv_file)
            self._write_header(csv_writer, authors)
            self._write_issues(csv_writer, sprint.issues, aggregated_work_log, authors)

    def _open_csv_writer(self, csv_file):
        return csv.writer(
            csv_file,
            delimiter=self._config.delimiter,
            lineterminator='\n',
            quotechar=self._config.quote_char,
            quoting=csv.QUOTE_MINIMAL)

    def _write_header(self, csv_writer, authors):
        header = [
            'Issue title',
            'Estimated time (min)',
            'Spent time (min)']
        header = header + authors

        csv_writer.writerow(header)

    def _write_issues(self, csv_writer, issues, aggregated_work_log, authors):
        idx_issue = 0
        secs_in_hour = 60 * 60

        for issue in issues:
            title = F'=HYPERLINK("{issue.url}"; "[{issue.key}] {issue.summary}")'
            estimated_time = issue.time_data.estimated_time / secs_in_hour
            spent_time = issue.time_data.spent_time / secs_in_hour

            record = [
                title,
                self._format_number(estimated_time),
                self._format_number(spent_time)]

            for author in authors:
                spent_time = 0
                if author in aggregated_work_log[idx_issue]:
                    spent_time = aggregated_work_log[idx_issue][author]
                    spent_time = spent_time / secs_in_hour
                record.append(self._format_number(spent_time))

            csv_writer.writerow(record)
            idx_issue = idx_issue + 1

    def _format_number(self, value):
        formatted_value = '{0:.1f}'.format(value)
        if self._config.use_comma_as_decimal_separator:
            formatted_value = formatted_value.replace('.', ',')

        return formatted_value
