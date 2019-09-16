class Issue:

    def __init__(self, key, summary, url, time_data):
        self._key = key
        self._summary = summary
        self._url = url
        self._time_data = time_data

    @property
    def key(self):
        return self._key

    @property
    def summary(self):
        return self._summary

    @property
    def url(self):
        return self._url

    @property
    def time_data(self):
        return self._time_data
