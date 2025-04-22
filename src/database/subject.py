import re
from database import DataObject

class Subject(DataObject):
    """
    Repräsentiert ein Unterichtsfach.

    :param abr: Abkürzung in der Datenbank (3 Buchstaben)
    :param name: Langbezeichnung (muss mit Großbuchstaben beginnen)
    """
    def __init__(self, abr:str, name:str):
        self.__abr:str = ''
        self.__name:str = ''

        re_abr = r'[A-Za-z]+'
        re_name = r'[A-Z][a-z]+'

        match_abr:list[str] = re.findall(re_abr, abr)
        match_name:list[str] = re.findall(re_name, name)

        if (match_abr) and len(match_abr[0]) == 3:
            self.__abr = match_abr[0].upper()

        if (match_name): self.__name = name

    @property
    def abr(self) -> str:
        ''':getter: Liefert die Abkürzung in der Datenbank'''
        return self.__abr

    @property
    def name(self) -> str:
        ''':getter: Liefert die Langbezeichnung des Faches'''
        return self.__name