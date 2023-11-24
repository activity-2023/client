class BadProtocol(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message


class BadConfig(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message


class BadData(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message


class IncorrectId(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message


class AccessError(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message

class BadPassword(Exception):
    def __init__(self, message: str):
        super().__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message
