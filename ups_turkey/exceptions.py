class UPSException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return repr(f'[{self.code}] {self.message}')