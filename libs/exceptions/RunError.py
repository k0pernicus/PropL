#Python3.4 - Antonin Carette

class RunError(Exception):
    """
    Base class for "run error..." exceptions
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
