class SprintInfo:

    def __init__(self, start_date, end_date):
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date
