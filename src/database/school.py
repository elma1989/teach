from database import Data, Subject

class School(Data):
    """
    Dient zur Verwaltung von Daten.
    """
    def __init__(self):
        self.__subjects: list[Subject]