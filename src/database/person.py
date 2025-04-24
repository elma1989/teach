import re
from datetime import datetime
from database import DataObject

class Person(DataObject):
    """
    Repräsentiert eine Person.

    :param fname: Vorname der Person
    :param lname: Nachname der Person
    :param birth_date: Geburtdatum (JJJJ-MM-TT)
    :param id: ID der Person (Standard: 0)
    """
    def __init__(self, fname:str, lname:str, birth_date:str, id:int = 0) -> None:
        super().__init__()
        self.__id = id
        self.__fname:str = ''
        self.__lname:str = ''
        self.__birth_date:datetime|None = None

        rename:str = r'[A-Z][a-z]+ ?-?'

        fnames:list[str]|None = re.findall(rename, fname)
        lnames:list[str]|None = re.findall(rename, lname)

        if fnames:
            for x in fnames:
                self.__fname += x

        if lnames:
            for x in lnames:
                self.__lname += x

        try: self.__birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError as e: print(e)

    @property
    def id(self) -> int:
        """
        Verwaltet die Personen-ID.

        :getter: Gibt den gespeicherten Wert der ID zurück
        :setter: Setzt die ID wenn diese bei Erstellung noch nicht bekannt war und in der Datenbank gesucht worden ist
        """
        return self.__id
    
    @id.setter
    def id(self, id:int) -> None:
        if id > 0:
            self.__id = id

    @property
    def fname(self) -> str:
        ''':getter: Liefert den Vornamen der Person'''
        return self.__fname
    
    @property
    def lname(self) -> str:
        """
        Verwaltet den Familiennamen einer Person

        :getter: Liefert den Familienname
        :setter: Ändert den Familienname
        """
        return self.__lname
    
    @lname.setter
    def lname(self, lname:str) -> None:
        rename:str = r'[A-z][a-z] ?-?'
        lnames:list[str]|None = re.findall(rename, lname)

        if lnames:
            self.__lname = ''
            for x in lnames:
                self.__lname += x

    @property
    def birth_date(self) -> datetime|None:
        """
        :getter: Liefert das Geburtsdatum der Person
        :return: Geburtdatum als datetime-Objekt, **None**, wenn im Konstruktor das Geburtdatum nicht im korrekten Format angegeben wurde
        """
        return self.__birth_date

    @property
    def db_birth(self) -> str:
        """
        :getter: Liefert das Geburtdatum einer Person
        :return: Geburtdatum (JJJJ-MM-TT) einer Person
        """
        return self.birth_date.strftime('%Y-%m-%d') if self.birth_date else ''
    
    def __repr__(self) -> str:
        return f'{self.fname} {self.lname}'
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Person): return False
        return self.fname == other.fname and self.lname == other.lname and self.birth_date == other.birth_date
    
    def to_dict(self) -> dict[str,str|int]:
        """
        Liefet die Daten einer Person zur Verarbeitung im Frontend.

        :return: Personendaten
        """
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'birthDate': self.db_birth
        }