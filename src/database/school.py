from database import Data, Error, Subject, Teacher

class School(Data):
    """
    Dient zur Verwaltung von Daten.
    """
    def __init__(self) -> None:
        self.__subjects: list[Subject]
        self.__teachers: list[Teacher]

    @property
    def subjects(self) -> list[Subject]:
        ''':getter: Liefert die aktuelle Fachliste'''
        sql = 'SELECT * FROM subject ORDER BY sub_abr'

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql)
                res = self.c.fetchall()
                self.__subjects = [Subject(row[0], row[1]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__subjects
    
    @property
    def teachers(self) -> list[Teacher]:
        sql:str = 'SELECT * FROM teacher ORDER BY teach_last_name, teach_first_name'

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql)
                res = self.c.fetchall()
                self.__teachers = [Teacher(row[1],row[2], row[3], row[0]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__teachers