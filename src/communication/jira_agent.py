import requests
from jira.client import GreenHopper
from tqdm import tqdm

from domain.issue import Issue
from domain.issue_time_data import IssueTimeData
from domain.sprint_info import SprintInfo
from domain.work_log_item import WorkLogItem


class JiraAgent:

    def __init__(self, server_url, username, password):
        self._server_url = server_url
        self._username = username
        self._password = password

        self._jira_client = None

    def connect(self):
        self._jira_client = GreenHopper(
            basic_auth=(self._username, self._password),
            options={'server': self._server_url})

    def retrieve_sprint_id(self, board_id, sprint_name):
        sprints_dto = self._jira_client.sprints(board_id)
        for sprint_dto in sprints_dto:
            if sprint_dto.name.strip() == sprint_name:
                return sprint_dto.id

        return ''

    def retrieve_sprint_info(self, sprint_id):
        response = requests.get(
            F'{self._server_url}/rest/agile/1.0/sprint/{sprint_id}',
            auth=(self._username, self._password))
        response_json = response.json()

        start_date = response_json['startDate'][:10]
        end_date = response_json['completeDate'][:10]

        return SprintInfo(start_date, end_date)

    def download_work_log_of_sprint(self, sprint_id):
        query = F'sprint={sprint_id} AND (type="Task" OR type="Sub-task" OR type="Bug") AND status="Done"'
        issues_dto = self._jira_client.search_issues(query, maxResults=160)

        return self._download_details_of_issues(issues_dto)

    def _download_details_of_issues(self, issues_dto):
        issues = []
        progress_bar = tqdm(total=issues_dto.total)

        for issue_dto in issues_dto:
            detailed_issue_dto = self._jira_client.issue(issue_dto.key)

            work_log = self._collect_work_log(detailed_issue_dto.fields.worklog.worklogs)
            time_data = IssueTimeData(
                issue_dto.fields.timeoriginalestimate or 0,
                issue_dto.fields.aggregatetimespent or 0,
                work_log)
            issue = Issue(issue_dto.key, issue_dto.fields.summary, issue_dto.permalink(), time_data)
            issues.append(issue)

            progress_bar.update(1)

        progress_bar.close()

        return issues

    def _collect_work_log(self, work_logs_dto):
        work_log_items = []

        for work_log_dto in work_logs_dto:
            author = work_log_dto.author.displayName
            comment = work_log_dto.comment
            creation_date = work_log_dto.created
            spent_time = work_log_dto.timeSpentSeconds

            work_log_item = WorkLogItem(author, creation_date, spent_time, comment)

            work_log_items.append(work_log_item)

        return work_log_items
