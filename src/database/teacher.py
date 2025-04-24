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
        self.__subject:list[Subject] = []
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