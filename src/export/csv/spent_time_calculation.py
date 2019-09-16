def summarize_spent_time_by_author(sprint):
    aggregated_work_log = []
    authors = set()

    for issue in sprint.issues:
        work_log = _summarize_spent_time_for_issue(sprint, issue, authors)
        aggregated_work_log.append(work_log)

    sorted_authors = list(authors)
    sorted_authors.sort()

    return aggregated_work_log, sorted_authors


def _summarize_spent_time_for_issue(sprint, issue, authors):
    work_log_for_issue = {}

    si = sprint.sprint_info
    work_logs = [entry for entry in issue.time_data.work_log
                 if si.start_date <= entry.creation_date and entry.creation_date <= si.end_date]

    for work_log_item in issue.time_data.work_log:
        author = work_log_item.author
        spent_time = work_log_item.spent_time

        work_log_for_issue.setdefault(author, 0)
        work_log_for_issue[author] = work_log_for_issue[author] + spent_time

        authors.add(author)

    return work_log_for_issue
