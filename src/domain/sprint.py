class Sprint:

    def __init__(self, sprint_info, issues):
        self._sprint_info = sprint_info
        self._issues = issues

    @property
    def issues(self):
        return self._issues

    @property
    def sprint_info(self):
        return self._sprint_info
