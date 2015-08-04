#Python3.4 - Antonin Carette

class FailToLoad(Exception):
    """
    Base class for "fail to load..." exceptions
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
