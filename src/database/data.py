from sqlite3 import connect, Connection, Cursor
from database import Error, DBPATH
class Data:
    """
    Stellt eine Datenbankverbindung zur Verfügung.
    """
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
    
    def connect(self) -> None:
        """
        Stellt eine Verbindung zur Datenbank her.
        """
        try:
            self.__con = connect(DBPATH)
            if self.con: self.__c = self.con.cursor()
        except Error as e: 
            print(e)
            if self.con:
                self.con.close()
                self.__con = None

    def close(self) -> None:
        """
        Trennt die Datenbankverbindung wieder.
        """
        if self.con and self.c:
            self.c.close()
            self.con.close()
            self.__c = None
            self.__con = None