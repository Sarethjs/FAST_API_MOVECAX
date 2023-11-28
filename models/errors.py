class DataNotInsertedException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'DataNotInserted: {self.message}'


class DatabaseNotOnlineException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'DatabaseNotOnline: {self.message}'


class CantParseDataToModel(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'Data not parsed: {self.message}'
