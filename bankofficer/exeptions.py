class DB2Exception(Exception):
    status = None

    def __init__(self, status=None):
        if status is not None:
            self.status = status

        super().__init__(self.status)