class CSRFTokenMissingException(Exception):
    
    def __init__(self, message):
        super().__init__(message)

class ContentNull(Exception):

    def __init__(self, message):
        super().__init__(message)

class InvalidArgument(Exception):

    def __init__(self, message):
        super().__init__(message)