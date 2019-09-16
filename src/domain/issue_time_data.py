class IssueTimeData:

    def __init__(self, estimated_time, spent_time, work_log):
        self._estimated_time = estimated_time
        self._spent_time = spent_time
        self._work_log = work_log

    @property
    def estimated_time(self):
        return self._estimated_time

    @property
    def spent_time(self):
        return self._spent_time

    @property
    def work_log(self):
        return self._work_log
