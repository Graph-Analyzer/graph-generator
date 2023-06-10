class InputError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InternalError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
