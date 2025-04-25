from database import Data, Error, Subject, Teacher, Grade, Student

class School(Data):
    """
    Dient zur Verwaltung von Daten.
    """
    def __init__(self) -> None:
        self.__subjects: list[Subject]
        self.__teachers: list[Teacher]
        self.__grades: list[Grade]

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
        '''
        :getter: Liefert eine Liste aller aktiver Lehrer.
        '''
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
    
    @property
    def grades(self) -> list[Grade]:
        ''':getter: liefert eine Liste aller Klassen'''
        sql:str = """SELECT g.grd_name, t.teach_first_name, t.teach_last_name, t.teach_birth_date, t.teach_id
            FROM grade g JOIN teacher t ON g.teach_id = t.teach_id
            ORDER BY g.grd_name"""
        
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql)
                res = self.c.fetchall()
                self.__grades = [Grade(row[0], Teacher(row[1],row[2],row[3],row[4])) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__grades

    def grades_of(self,leader:Teacher) -> list[Grade]:
        """
        Zeigt alle Klassen eines Lehrers

        :param leader: Instanz des Klassenleiters
        :return: Klassenliste alphabetischer Ordnung
        """
        grades:list[Grade] = []
        sql:str = 'SELECT grd_name FROM grade WHERE teach_id = ? ORDER BY grd_name'

        if not isinstance(leader,Teacher) or not leader.exists(): return []

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (leader.id,))
                res = self.c.fetchall()
                grades = [Grade(row[0], leader) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return grades
    
    def students(self, grade:Grade|None) -> list[Student]|None:
        """
        Liefert eine Liste von Schülern aus einer Klasse.

        :param grade: Klasse aus der die Schüler stammen, wird **None** übergeben, wird nach Schülern ohne Klassenzuordnung gesucht
        :return: Liste mit Schülern aus der Klasse, kann die Klasse nicht gefunden werden, wird **None** zurückgegen
        """
        students:list[Student] = []
        sql:list[str] = [
            """SELECT std_frist_name, std_last_name, std_birth_date, std_id
                FROM student WHERE grd_name = ? ORDER BY std_last_name, std_first_name""",
            """SELECT std_frist_name, std_last_name, std_birth_date, std_id
                FROM student WHERE grd_name IS NULL ORDER BY std_last_name, std_first_name"""
        ]

        if isinstance(grade, Grade):
            if not grade.exists(): return None
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql[0], (grade.name,))
                    res = self.c.fetchall()
                    students = [Student(row[0], row[1], row[2], row[3]) for row in res]
            except Error as e: print(e)
            finally: self.close()

        if not grade:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql[1])
                    res = self.c.fetchall()
                    students = [Student(row[0], row[1], row[2], row[3]) for row in res]
            except Error as e: print(e)
            finally: self.close()

        return students

    
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