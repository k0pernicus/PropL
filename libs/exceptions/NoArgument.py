class NoArgument(Exception):
    """
    Base class for "no argument..." exceptions
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
