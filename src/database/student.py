from database import Person, Grade, Error, FKON

class Student(Person):
    """
    Repräsentiert einen Schüler.

    :param fname: Vorname des Schülers
    :param lname:  Nachname des Schülers
    :param birth_date: Geburtsdatum (JJJJ-MM-TT) des Schülers
    :param id: ID des Schülers (Standard: 0)
    :ivar grade: Instaz der zugeörigen Klasse (Standard: None)
    """
    def __init__(self,fname:str,lname:str,birth_date:str, id:int=0):
        super().__init__(fname, lname, birth_date, id)
        self.__grade:Grade|None = None

    @property
    def grade(self) -> Grade|None:
        """
        Verwaltet die Klasse des Schülers.

        :getter: Liefert die Klasse
        :setter: Legt die Klasse fest
        :return: **None**, wenn dem Schüler keine Klasse zugewiesen ist
        """
        sql:str = 'SELECT grd_name FROM student WHERE std_id = ?'
        self.__grade = None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.id,))
                res = self.c.fetchone()
                if res and res[0]: self.__grade = Grade(res[0])
        except Error as e: print(e)
        finally: self.close()

        return self.__grade
    
    @grade.setter
    def grade(self, grade:Grade):
        sql:str = "UPDATE student SET grd_name = ? WHERE std_id = ?"

        if isinstance(grade, Grade) and grade.exists():
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(FKON)
                    self.c.execute(sql,(grade.name, self.id))
                    self.con.commit()
                    self.__grade = grade
            except Error as e: print(e)
            finally: self.close()

    def exists(self) -> bool:
        """
        Prüft, ob ein Schüler bereits existiert.

        :return: **True**, wenn der Schüler bereits vorhanden ist
        """
        sql:str = """SELECT * FROM student
            WHERE std_first_name = ? AND std_last_name = ? AND std_birth_date = ?"""
        success:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.fname, self.lname, self.db_birth))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success

    def add(self) -> int:
        """
        Fügt einen neuen Schüler in die Datenbank ein.

        :return:
             | 0 - Erfolgreich
             | 1 - Ungültige Daten
             | 3 - Schüler bereits vorhanden
        """
        sql:list[str] = [
            'INSERT INTO student VALUES(NULL,?,?,?,NULL)',
            """SELECT std_id FROM student
                WHERE std_first_name = ? AND std_last_name = ? AND std_birth_date = ?"""
        ]
        success:bool = False

        if len(self.fname) == 0 or len(self.lname) == 0 or not self.birth_date: return 1
        if self.exists(): return 3

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql[0],(self.fname, self.lname, self.db_birth))
                self.con.commit()
                self.c.execute(sql[1], (self.fname, self.lname, self.db_birth))
                res = self.c.fetchone()
                if res: self.id = res[0]
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1
    
    def remove(self) -> int:
        """
        Löscht einen Schüler.

        :return:
             | 0 - Erfolgreich
             | 1 - Schüler nicht vorhanden
        """
        sql:str = 'DELETE FROM student WHERE std_id = ?'
        success:bool = False

        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql, (self.id,))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1