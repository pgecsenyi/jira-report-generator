class WorkLogItem:

    def __init__(self, author, creation_date, spent_time, comment):
        self._author = author
        self._creation_date = creation_date
        self._spent_time = spent_time
        self._comment = comment

    @property
    def author(self):
        return self._author

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def comment(self):
        return self._comment

    @property
    def spent_time(self):
        return self._spent_time
