from database import Person, Error, Subject

class Teacher(Person):
    """
    Repräsentiert einen Lehrer.

    :param fname: Vorname des Lehrers
    :param lname: Nachnmame des Leherers
    :param brith_date: Geburtsdatum (JJJJ-MM-TT) des Lehrers
    :param id: ID des Lehrers (Standard: 0)
    """
    def __init__(self, fname:str, lname:str, birth_date:str, id:int = 0) -> None:
        super().__init__(fname, lname, birth_date, id)
        self.__subjects:list[Subject] = []
        sql:str = """SELECT teach_id FROM teacher
            WHERE teach_first_name = ? AND teach_last_name = ? AND teach_birth_date = ?"""
        
        if self.id == 0:
            try:
                self.connct()
                if self.con and self.c:
                    self.c.execute(sql, (self.fname, self.lname, self.db_birth))
                    res = self.c.fetchone()
                    if res: self.id = res[0]
            except Error as e: print(e)
            finally: self.close()

    def subjects(self) -> list[Subject]:
        """
        Liefert alle Fächer eines Lehrers.

        :return: Fächerliste
        """
        sql:str = """SELECT s.sub_abr, s.sub_name
            FROM subject s JOIN teacher_subject ts ON t.sub_abr = ts.sub_abr
            WHERE ts.teach_id = ?
            ORDER BY s.sub_abr"""
        
        if self.id == 0: return []

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.id,))
                res = self.c.fetchall()
                self.__subjects = [Subject(row[0], row[1]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__subjects