from sqlite3 import connect, Connection, Cursor
from database import Error
class Data:
    """
    Stellt eine Datenbankverbindung zur Verfügung
    """
    DBPATH:str = '../teach.db'

    def __init__(self) -> None:
        self.__con:Connection|None = None
        self.__c:Cursor|None = None

    @property
    def con(self) -> Connection|None:
        """
        Verwaltet die Datenbankverbindung.

        :getter: Stellt die Databankverbindung bereit
        :return: **None**, wenn keine Verbindung beteht
        """
        return self.__con
    
    @property
    def c(self) -> Cursor|None:
        """
        Verwaltet den Datenbankzeiger.

        :getter: Verweist auf den Datenbankzeiger
        :return: **None**, wenn dieser noch nicht gesetzt ist
        """
        return self.__c