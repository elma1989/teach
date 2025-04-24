import re
from datetime import datetime
from database import DataObject

class Person(DataObject):
    """
    Repräsentiert eine Person.

    :param fname: Vorname der Person
    :param lname: Nachname der Person
    :param birth_date: Geburtdatum (JJJJ-MM-TT)
    """
    def __init__(self, fname:str, lname:str, birth_date:str) -> None:
        self.__fname:str = ''
        self.__lname:str = ''
        self.__birth_date:datetime|None = None

        rename:str = r'[A-Z][a-z] ?-?'

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