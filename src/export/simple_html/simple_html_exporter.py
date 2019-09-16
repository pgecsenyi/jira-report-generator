from jinja2 import Environment, PackageLoader, select_autoescape, Template
import os

from export.exporter import Exporter
from export.simple_html.simple_html_analyser import SimpleHtmlAnalyser
from export.simple_html.jinja_filters import secs_to_hours

TEMPLATE_FILE_NAME = 'work_time_report.html'


class SimpleHtmlExporter(Exporter):

    def export(self, filename, sprint):
        self._output_path = filename
        self._sprint = sprint
        self._template_data = {}

        self._prepare_summary()
        report = self._build_report()
        self._save_output(report)

    def _prepare_summary(self):
        analyser = SimpleHtmlAnalyser(self._sprint)
        analyser.collect_data()

        self._template_data['authors'] = analyser.author_names
        self._template_data['details_by_authors'] = analyser.details_by_authors
        self._template_data['issues'] = analyser.issues
        self._template_data['summary'] = analyser.summary

    def _build_report(self):
        env = Environment(
            loader=PackageLoader('asset', 'template/simple_html'),
            autoescape=select_autoescape(['html', 'xml']))
        env.filters['secs_to_hours'] = secs_to_hours

        tm = env.get_template(TEMPLATE_FILE_NAME)

        return tm.render(self._template_data)

    def _save_output(self, content):
        with open(self._output_path, 'w', encoding='utf-8') as output_file:
            return output_file.write(content)
