from database import Person, Grade, Error, FKON

class Student(Person):
    """
    Repräsentiert einen Schüler.

    :param fname: Vorname des Schülers
    :param lname:  Nachname des Schülers
    :param birth_date: Geburtsdatum (JJJJ-MM-TT) des Schülers
    :param id: ID des Schülers (Standard: 0)
    :param grade: Instaz der zugeörigen Klasse (Standard: None)
    """
    def __init__(self,fname:str,lname:str,birth_date:str, id:int=0, grade:Grade|None = None):
        super().__init__(fname, lname, birth_date, id)
        self.__grade = grade if isinstance(grade, Grade) and grade.exists() else None
        sql:str = """SELECT std_id, grd_name FROM student
            WHERE std_first_name = ? AND std_last_name = ? AND std_birth_date = ?"""
        
        if not grade or id == 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql, (self.fname, self.lname, self.db_birth))
                    res = self.c.fetchone()
                    if res:
                        self.id = res[0]
                        self.__grade = Grade(res[1])
            except Error as e: print(e)
            finally: self.close()