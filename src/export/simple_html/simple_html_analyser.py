from export.simple_html.work_type_categorization import categorize_work_log_item
from domain.work_types import OTHER


class SimpleHtmlAnalyser:

    def __init__(self, sprint):
        self._sprint = sprint

        self._author_names = []
        self._details_by_authors = {}
        self._issues = {}
        self._summary = {}
        self._unsorted_author_names = set()

    @property
    def author_names(self):
        return self._author_names

    @property
    def details_by_authors(self):
        return self._details_by_authors

    @property
    def issues(self):
        return self._issues

    @property
    def summary(self):
        return self._summary

    def collect_data(self):
        for issue in self._sprint.issues:
            issue_summary = self._create_issue_summary(issue)
            self._issues[issue.key] = issue_summary

            self._process_issue(issue)

        self._finalize_report()

    def _process_issue(self, issue):
        issue_summary = self._issues[issue.key]
        authors_involved = set()
        si = self._sprint.sprint_info

        work_logs = [entry
                     for entry
                     in issue.time_data.work_log
                     if si.start_date <= entry.creation_date and entry.creation_date <= si.end_date]

        for work_log_item in work_logs:
            author = work_log_item.author
            spent_time = work_log_item.spent_time

            self._add_to_key(issue_summary['spent_time_by_author'], author, spent_time)
            self._add_to_key(issue_summary, 'spent_time', spent_time)
            self._add_to_key(self._summary, 'spent_time', spent_time)
            self._add_to_author(issue.key, work_log_item)

            self._unsorted_author_names.add(author)
            authors_involved.add(author)

        self._add_to_key(self._summary, 'estimated_time', issue_summary['estimated_time'])
        self._add_estimation_to_authors(authors_involved, issue)

    def _create_issue_summary(self, issue):
        return {
            'title': F'[{issue.key}] {issue.summary}',
            'estimated_time': issue.time_data.estimated_time,
            'spent_time': 0,
            'spent_time_by_author': {},
            'url': issue.url
        }

    def _add_to_key(self, dictionary, key, value):
        dictionary.setdefault(key, 0)
        dictionary[key] = dictionary[key] + value

    def _add_to_author(self, issue_id, work_log_item):
        author = work_log_item.author
        category = categorize_work_log_item(work_log_item)

        self._create_author_details(author, issue_id)

        summary = self._details_by_authors[author]['summary']
        summary[category] = summary[category] + work_log_item.spent_time
        summary['sum'] = summary['sum'] + work_log_item.spent_time

        task_details = self._details_by_authors[author]['tasks'][issue_id]
        task_details[category] = task_details[category] + work_log_item.spent_time
        task_details['sum'] = task_details['sum'] + work_log_item.spent_time

    def _create_author_details(self, author, issue_id):
        wtc = self._create_default_work_time_categories()
        self._details_by_authors.setdefault(author, {'summary': wtc, 'tasks': {}})

        wtc = self._create_default_work_time_categories()
        self._details_by_authors[author]['tasks'].setdefault(issue_id, wtc)

    def _create_default_work_time_categories(self):
        return {
            'help': 0,
            'implementation': 0,
            'other': 0,
            'review': 0,
            'sum': 0
        }

    def _add_estimation_to_authors(self, authors_involved, issue):
        for author in authors_involved:
            summary = self._details_by_authors[author]['summary']
            summary.setdefault('estimated_time', 0)
            summary['estimated_time'] += issue.time_data.estimated_time

    def _finalize_report(self):
        self._calculate_author_percentages()
        self._sort_authors()

    def _calculate_author_percentages(self):
        for author in self._unsorted_author_names:
            details = self._details_by_authors[author]
            sum = 0
            summary = details['summary']

            details['summary_percentage'] = {}

            for category in details['summary']:
                if category is not 'sum' and category is not 'estimated_time':
                    percentage = int(summary[category] / summary['sum'] * 100)
                    details['summary_percentage'][category] = percentage
                    sum = sum + percentage

            details['summary_percentage'][OTHER] = details['summary_percentage'][OTHER] + (100 - sum)

    def _sort_authors(self):
        sorted_author_names = list(self._unsorted_author_names)
        sorted_author_names.sort()
        self._author_names = sorted_author_names
