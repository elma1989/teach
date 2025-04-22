import re
from database import DataObject, Error

class Subject(DataObject):
    """
    Repräsentiert ein Unterichtsfach.

    :param abr: Abkürzung in der Datenbank (3 Buchstaben)
    :param name: Langbezeichnung (muss mit Großbuchstaben beginnen)
    """
    def __init__(self, abr:str, name:str):
        self.__abr:str = ''
        self.__name:str = ''

        re_abr:str = r'[A-Za-z]+'
        re_name:str = r'[A-Z][a-z]+'

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

    def __repr__(self) -> str: return self.abr

    def __eq__(self, other) -> bool:
        if not isinstance(other, Subject): return False
        return self.abr == other.abr

    def exists(self) -> bool:
        """
        Prüft, ob das Unterrichtfach bereits existiert.

        :return: **True**, wenn das Fach bereits vorhanden ist
        """
        sql:str = 'SELECT * FROM subject WHERE sub_abr = ?'
        success:bool = False

        if len(self.abr) == 0: return False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.abr,))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success

    def add(self) -> int:
        """
        Fügt ein neues Fach zur Datenbank hinzu.

        :return:
             | 0 - erfolgreich
             | 1 - Ungrültige Daten
             | 3 - Fach bereits vorhanden
        """
        sql:str = 'INSERT INTO subject VALUES(?,?)'
        success:bool = False

        if len(self.abr) == 0 or len(self.name) == 0: return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.abr, self.name))
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3
    
    def remove(self) -> int:
        return 1
    
    def to_dict(self) -> dict[str,str]:
        return {}