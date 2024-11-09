class DBFException(Exception):
    def __init__(self, message):
        super().__init__(str(message))
        self.add_note("There was an error in the mapper")


class NotFoundTable(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.add_note("The table was not found in the .dbf database")


class InvalidAnnotatedType(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.add_note("The table was not found in the .dbf database")


class DatabaseNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.add_note("The database was not found.")
