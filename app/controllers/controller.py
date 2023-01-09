class Controller(object):
    def __init__(request, db, **kwargs):
        self._db = db
        self._request = request
        self._options = kwargs
