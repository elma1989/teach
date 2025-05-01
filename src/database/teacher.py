from database import Person, Error, Subject, FKON

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
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql, (self.fname, self.lname, self.db_birth))
                    res = self.c.fetchone()
                    if res: self.id = res[0]
            except Error as e: print(e)
            finally: self.close()

    @property
    def subjects(self) -> list[Subject]:
        """
        Liefert alle Fächer eines Lehrers.

        :return: Fächerliste
        """
        sql:str = """SELECT s.sub_abr, s.sub_name
            FROM subject s JOIN teacher_subject ts ON s.sub_abr = ts.sub_abr
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
    
    def exists(self) -> bool:
        """
        Prüft, ob ein Lehrer bereits vorhanden ist.

        :return: **True**, wenn der Lehrer bereits vorhanden ist
        """
        sql:str = """SELECT * FROM teacher
            WHERE teach_first_name = ? AND teach_last_name = ? AND teach_birth_date = ?"""
        success:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.fname, self.lname, self.db_birth))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success

    def add(self) -> int:
        """
        Fügt einen Lehrer zur Datenbank hinzu.

        :return:
             | 0 - Erfolgreich
             | 1 - Daten ungültig
             | 3 - Lehrer bereits vorhanden
        """
        sql:list[str] = [
            'INSERT INTO teacher VALUES(NULL,?,?,?)',
            """SELECT teach_id FROM teacher
                WHERE teach_first_name = ? AND teach_last_name = ? AND teach_birth_date = ?"""
        ]
        success:bool = False

        if len(self.fname) == 0 or len(self.lname) == 0 or not self.birth_date: return 1
        if self.exists(): return 3
        
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql[0], (self.fname, self.lname, self.db_birth))
                self.con.commit()
                self.c.execute(sql[1], (self.fname, self.lname, self.db_birth))
                res = self.c.fetchone()
                if res: self.id = int(res[0])
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1
    
    def remove(self) -> int:
        """
        Löscht einen Lehrer.

        :return:
             | 0 - Erfolgreich
             | 1 - Lehrer nicht vorhanden
             | 2 - Lehrer leitet noch Klassen und/oder Kursee
        """
        sql:str = 'DELETE FROM teacher WHERE  teach_id = ?'
        success:bool = False

        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.id,))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 2
    
    def add_subject(self, sub:Subject) -> int:
        """
        Fügt dem Lehrer ein neues Fach hinzu.

        :param sub: zu hinzufügendes Fach
        :return: 
             | 0 - Erfolreich
             | 1 - Fach nicht gefunden
             | 2 - Fach bereits vorhanden
        """
        sql:str = 'INSERT INTO teacher_subject VALUES(?,?)'
        success:bool = False

        if not isinstance(sub,Subject) or not sub.exists(): return  1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.id, sub.abr))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 2
    
    def del_subject(self, sub:Subject) -> int:
        """
        Löscht ein Fach eines Lehrers.

        :param sub: Zu löschendes Fach
        :return:
             | 0 - Erfolgreich
             | 1 - Fach oder Lehrer nicht gefunden
             | 2 - der Lehrer leitet noch ein Kurs von dem Fach
        """
        sql:list[str] = [
            """SELECT sub_abr FROM course
                WHERE teach_id = ? AND sub_abr = ?""",
            'DELETE FROM teacher_subject WHERE teach_id = ? AND sub_abr = ?'
        ]
        act_crs:bool = False
        success:bool = False
        
        if not self.exists(): return 1
        if not isinstance(sub, Subject) or not sub.exists(): return 1
        if not sub in self.subjects: return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql[0],(self.id, sub.abr))
                res = self.c.fetchone()
                if res: act_crs = True
                if not act_crs:
                    self.c.execute(sql[1], (self.id, sub.abr))
                    self.con.commit()
                    success = True
        except Error as e: print(e)
        finally: self.close()

        if act_crs: return 2
        return 0 if success else 1