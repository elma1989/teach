from typing import Any
from database import DataObject, Teacher, Subject, Student, Error, FKON

class Course(DataObject):
    """
    Respäsentiert einen Kurs.

    :param name: Kursname
    :param leader: Lehrerinstanz des Klassenleiters (Standard: None)
    :param subject: Instanz des Faches (Standard: None)
    :ivar students: Mitgliederlieste
    """
    def __init__(self, name:str, leader:Teacher|None=None, subject:Subject|None=None) -> None:
        self.__name = name
        self.__leader:Teacher|None = None
        self.__subject:Subject|None = None 
        self.__students:list[Student] = []
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

        if isinstance(leader, Teacher) and self.subject in leader.subjects:
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

    @property
    def students(self) -> list[Student]:
        ''':getter: Liefert alle Kursteilnehmer alphbetischer Ordnung'''
        sql:str = """SELECT s.std_first_name, s.std_last_name, s.std_birth_date, s.std_id
            FROM student_course sc JOIN student s ON sc.std_id = s.std_id
            WHERE sc.crs_name = ? ORDER BY s.std_last_name, s.std_first_name"""
        
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name,))
                res = self.c.fetchall()
                self.__students = [Student(row[0], row[1], row[2], row[3]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__students

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
             | 2 - Leiter oder Fach existieren nicht
             | 3 - Kurs ist bereits vorhanden
        """
        sql:str = 'INSERT INTO course VALUES(?,?,?)'
        success:bool = False

        if not isinstance(self.leader, Teacher) or not isinstance(self.subject, Subject): return 2
        if not self.subject.exists() or not self.subject in self.leader.subjects: return 2
        
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name, self.leader.id, self.subject.abr))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3
    
    def remove(self) -> int:
        """
        Löscht einen Kurs.

        :return:
             | 0 - Erfolgreich
             | 1 - Kurs nicht vorhanden
        """
        sql:str = 'DELETE FROM course WHERE crs_name = ?'
        success:bool = False

        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql, (self.name,))
                self.con.commit()
                success = True
        except Error as e:print(e)
        finally: self.close()

        return 0 if success else 1
    
    def to_dict(self) -> dict[str,Any]:
        """
        Liefert die Kerndaten eines Kurses.

        :return: Wörterbuch des Kurses
        """    
        outdict:dict[str,Any] = {'name':self.name}
        if self.subject: outdict['subject'] = self.subject.to_dict()
        return outdict
    
    def add_student(self, std:Student) -> int:
        """
        Fügt einen Schüler zur Datenbank hinzu.

        :param std: zu hinzufügender Schüler
        :return:
             | 0 - Erfolgreich
             | 1 - Übertragenes Objekt ist kein Schüler
             | 2 - Schüler ist nicht vorhanden
             | 3 - Schüler ist bereits in dem Kurs eingetragen
        """
        sql:str = 'INSERT INTO student_course VALUES(?,?)'
        success:bool = False

        if not isinstance(std, Student): return 1
        if not std.exists(): return 2

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(std.id, self.name))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3