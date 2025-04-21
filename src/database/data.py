from sqlite3 import connect, Connection, Cursor
from abc import ABC, abstractmethod
from typing import Any
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

class DataObject(Data, ABC):
    """
    Repräsentiert eine Datenbankentität.
    """
    def __init__(self):
        Data.__init__()

    @abstractmethod
    def exists(self) -> bool: 
        """
        Prüft, ob das aktuelle Objekt exitiert.

        :return: **True**, wenn das Objekt bereits vorhanden ist
        """
        pass

    @abstractmethod
    def add(self) -> int: 
        """
        Fügt ein neues Objekt zur Datenbank hinzu.

        :return:
             | 0 - erfolgreich
             | 1 - Daten sind nicht Validiert oder nicht im gültigen Format
             | 2 - Beziehende Referenzen sind nicht vorhanden
             | 3 - Objekt existiert bereits
        """
        pass

    @abstractmethod
    def remove(self) -> int:
        """
        Löscht das akuelle Objekt aus der Datenbank.

        :return:
            | 0 - erfolgreich
            | 1 - Objekt ist nicht Vorhanden
            | 2 - Objekt kann nicht gelöscht werden, da noch Referenzen vorhanden sind
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Liefert die Attibute des Objektes für das Frontend.

        :return: Daten als Wörterbuch
        """