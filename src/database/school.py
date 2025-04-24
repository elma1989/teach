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
    
    def getTeacher(self, id:int) -> Teacher|None:
        """
        Sucht einen Lehrer in der Datenbank.

        :param id: ID des Lehrers
        :return: Instanz des Lehrers, **None**, wenn kein Lehrer gefunden wurde
        """
        teacher:Teacher|None = None
        sql:str = 'SELECT * FROM teacher WHERE teach_id = ?'

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (id,))
                res = self.c.fetchone()
                if res: teacher = Teacher(res[1], res[2], res[3], res[0])
        except Error as e: print(e)
        finally: self.close()

        return teacher