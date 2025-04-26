from database import DataObject, Teacher, Subject, Error, FKON

class Course(DataObject):
    """
    Respäsentiert einen Kurs.

    :param name: Kursname
    :param leader: Lehrerinstanz des Klassenleiters (Standard: None)
    :param subject: Instanz des Faches (Standard: None)
    """
    def __init__(self, name:str, leader:Teacher|None=None, subject:Subject|None=None) -> None:
        self.__name = name
        self.__leader:Teacher|None = None
        self.__subject:Subject|None = None 
        sql:str = """SELECT t.teach_first_name, t.teach_last_name, t.teach_birth_date, t.teach_id, s.sub_abr, s.sub_name
            FROM course c JOIN teacher t ON c.teach_id = t.teach_id
            JOIN subject s ON c.sub_abr = s.sub_abr
            WHERE c.crs_name = ?"""
        
        if isinstance(leader, Teacher) and leader.exists(): self.__leader = leader
        if isinstance(subject, Subject) and subject.exists(): self.__subject = subject

        if not self.__leader or not self.__subject:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(name,))
                    res = self.c.fetchone()
                    if res:
                        self.__leader = Teacher(res[0], res[1], res[2], res[3])
                        self.__subject = Subject(res[4], res[5])
            except Error as e: print(e)
            finally: self.close()

    @property
    def name(self) -> str:
        """
        :getter: Liefet den Namen des Kurses
        """
        return self.__name

    @property
    def leader(self) -> Teacher|None:
        """
        Verwaltet den Kursleiter.

        :getter: Liefert den Kursleiter
        :setter: Wechselt den Kursleiter
        """
        return self.__leader

    @leader.setter
    def leader(self,leader:Teacher) -> None:
        sql:str = 'UPDATE course SET teach_id = ? WHERE crs_name = ?'

        if isinstance(leader, Teacher):
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(FKON)
                    self.c.execute(sql,(leader.id, self.name))
                    self.con.commit()
                    self.__leader = leader
            except Error as e: print(e)
            finally: self.close()
    
    @property
    def subject(self) -> Subject|None:
        ''':getter: Liefert das Fach des Kurses'''
        return self.__subject

    def __repr__(self) -> str: return self.name

    def __eq__(self,other) -> bool:
        if not  isinstance(other, Course): return False
        return self.name == other.name

    def exists(self) -> bool:
        """
        Prüft, ob der Kurs bereits vorhanden ist.

        :return: **True**, wenn der Kurs bereits vorhanden ist
        """
        sql:str = 'SELECT * FROM course WHERE crs_name = ?'
        success:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name,))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success
    
    def add(self) -> int:
        """
        Fügt einen neuen Kurs in die Datenbank ein.

        :return:
             | 0 - Erfolgreich
             | 1 - Nicht Korrekte Datenstruktur
             | 2 - Leiter oder Fach existieren nicht
             | 3 - Kurs ist bereits vorhanden
        """
        sql:str = 'INSERT INTO course VAULES(?,?,?)'
        success:bool = False

        if not isinstance(self.leader, Teacher) or not isinstance(self.subject, Subject): return 1
        if not self.leader.exists() or not self.subject.exists(): return 2

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name, self.leader.id, self.subject.abr))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3