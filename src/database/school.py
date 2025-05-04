from database import Data, Error, Subject, Teacher, Grade, Student, Course, Lesson

class School(Data):
    """
    Dient zur Verwaltung von Daten.
    """
    def __init__(self) -> None:
        self.__subjects: list[Subject] = []
        self.__teachers: list[Teacher] = []
        self.__grades: list[Grade] = []
        self.__courses: list[Course] = []

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
    
    @property
    def courses(self) -> list[Course]:
        ''':getter: Liefert eine Liste von allen in der Schule angebotenen Kursen'''
        sql:str = 'SELECT crs_name FROM course ORDER BY crs_name'
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql)
                res = self.c.fetchall()
                self.__courses = [Course(row[0]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return self.__courses

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

    def grades_of(self,leader:Teacher) -> list[Grade]|None:
        """
        Zeigt alle Klassen eines Lehrers

        :param leader: Instanz des Klassenleiters
        :return: Klassenliste alphabetischer Ordnung, **None**, wenn der Lehrer nicht existiert
        """
        grades:list[Grade] = []
        sql:str = 'SELECT grd_name FROM grade WHERE teach_id = ? ORDER BY grd_name'

        if not isinstance(leader,Teacher) or not leader.exists(): return None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (leader.id,))
                res = self.c.fetchall()
                grades = [Grade(row[0], leader) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return grades
    
    def getStudent(self, id:int) -> Student|None:
        """
        Sucht einen Schüler anhand der ID.

        :param id: ID des Schülers
        :return: Instanz des Schülers, **None**, wenn der Schüler nicht gefunden wurde
        """
        student:Student|None = None
        sql:str = """SELECT std_first_name, std_last_name, std_birth_date, std_id 
            FROM student WHERE std_id = ?"""

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(id,))
                res = self.c.fetchone()
                if res: student = Student(res[0], res[1], res[2], res[3])
        except Error as e: print(e)
        finally: self.close()

        return student
    
    def students(self, grade:Grade|None) -> list[Student]|None:
        """
        Liefert eine Liste von Schülern aus einer Klasse.

        :param grade: Klasse aus der die Schüler stammen, wird **None** übergeben, wird nach Schülern ohne Klassenzuordnung gesucht
        :return: Liste mit Schülern aus der Klasse, kann die Klasse nicht gefunden werden, wird **None** zurückgegen
        """
        students:list[Student] = []
        sql:list[str] = [
            """SELECT std_first_name, std_last_name, std_birth_date, std_id
                FROM student WHERE grd_name = ? ORDER BY std_last_name, std_first_name""",
            """SELECT std_first_name, std_last_name, std_birth_date, std_id
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

    def courses_of(self, leader:Teacher) -> list[Course]|None:
        """
        Liefet eine Liste von Kursen eines Lehrers.

        :param leader: Lehrerinstanz, bei der der Lehrer Kursleiter ist.
        :return: Kursliste mit allen Kursen, bei denen der übergebene Lehrer der Kursleiter ist,
            **None**, wenn der Lehrer nicht existiert
        """
        courses:list[Course] = []
        sql:str = 'SELECT crs_name FROM course WHERE teach_id = ? ORDER BY crs_name'

        if not isinstance(leader, Teacher) or not leader.exists(): return None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(leader.id,))
                res = self.c.fetchall()
                courses = [Course(row[0]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return courses

    def lessons(self, course:Course) -> list[Lesson]|None:
        """
        Liefert eine Lieste mit den Stunden eines Kurse.

        :param course: Kurs, zu dem die Stunden gesucht werden sollen
        :return: Liste mit den Stunden, **None**, wenn der Kurs nicht gefunden wurde
        """
        lessons:list[Lesson] = []
        sql:str = """SELECT les_time, les_topic FROM lesson
            WHERE crs_name = ? ORDER BY les_time"""

        if not isinstance(course, Course) or not course.exists(): return None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(course.name,))
                res = self.c.fetchall()
                lessons = [Lesson(course, row[0], row[1] if row[1] else '') for row in res]
        except Error as e: print(e)

        return lessons