from datetime import datetime
from database import DataObject, Course, Student, Error, FKON

class Lesson(DataObject):
    """
    Repräsentiert eine Unterrichstunde.

    :param course: Zugehöriger Kurs
    :param time: Geplanter Unterrichtsbeginn (JJJJ-TT-MM HH:MM)
    :param topic: Thema der Stunde (Standard: "")
    """
    def __init__(self, course:Course, time:str, topic:str = '') -> None:
        self.__course:Course|None = course if isinstance(course, Course) and course.exists() else None
        self.__time:datetime|None = None
        self.__topic:str = topic
        self.__homeworks:list[str] = []
        self.__students:list[tuple[Student,bool]] = []

        try:
            self.__time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        except ValueError as e: print(e)

    @property
    def course(self) -> Course|None:
        ''':getter: Liefert den aktuellen Kurs'''
        return self.__course
    
    @property
    def db_time(self) -> str:
        """
        :getter: Liefert die Datenbankzeit der Stunde
        :return: Zeit (JJJJ-MM-TT HH:MM)
        """
        return self.time.strftime('%Y-%m-%d %H:%M') if self.time else ''

    @property
    def time(self) -> datetime|None:
        """
        Verwaltet den Unterrichtsbeginn.

        :getter: Liefert den Unterrichtsbeginn
        :setter: Ändert den Unterrichtsbeginn (JJJJ-MM-TT HH:MM)
        :return: datetime-Objekt des Unterrichtsbegins
        """
        return self.__time
    
    @time.setter
    def time(self,time:str) -> None:
        sql:str = """UPDATE lasson SET les_time = ?
            WHERE crs_name = ? AND les_time = ?"""
        new_time:datetime|None = None

        if self.course and self.time:
            try:
                new_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
                self.connect()
                if self.con and self.c:
                    self.c.execute(FKON)
                    self.c.execute(sql,(time, self.course.name, self.db_time))
                    self.con.commit()
                    self.__time = new_time
            except Error as e: print(e)
            finally: self.close()

    @property
    def topic(self) -> str:
        """
        Vervaltet das Thema der Stunde.

        :getter: Liefert das Thema
        :setter: Legt des Thema fest
        """
        return self.__topic

    @topic.setter
    def topic(self, topic) -> None:
        sql:str = 'UPDATE lesson SET les_topic = ? WHERE crs_name = ? AND les_time = ?'

        if self.course and self.time:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(topic, self.course.name, self.db_time))
                    self.con.commit()
                    self.__topic = topic
            except Error as e: print(e)
            finally: self.close()

    @property
    def homeworks(self) -> list[str]:
        ''':getter: Liefert ale zu der Stunde aufgetragenen Hausaufgaben'''
        sql:str = """SELECT les_homework FROM lesson_homework
            WHERE crs_name = ? AND les_time = ?"""
        
        if isinstance(self.course, Course) and self.time:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(self.course.name, self.db_time))
                    res = self.c.fetchall()
                    self.__homeworks = [row[0] for row in res]
            except Error as e: print(e)
            finally: self.close()

        return self.__homeworks
    
    @property
    def students(self) -> list[tuple[Student,bool]]:
        ''':getter: Liefert eine Liste der Studenten und dem Anwensenheitsstatus (**True** = anwesend)'''
        sql:str = """SELECT s.std_first_name, s.std_last_name, s.std_birth_date, s.std_id, ls_student_present
            FROM student s JOIN lesson_student ls ON s.std_id = ls.std_id
            WHERE ls.crs_name = ? AND ls.les_time = ?
            ORDER BY s.std_last_name, s.std_first_name"""
        
        if self.course and self.time:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql, (self.course.name, self.db_time))
                    res = self.c.fetchall()
                    self.__students = [(Student(row[0], row[1], row[2], row[3]), bool(row[4])) for row in res]
            except Error as e: print(e)
            finally: self.close()

        return self.__students
    
    def __repr__(self) -> str:
        return f'{self.course.name}: {self.db_time}' if self.course and self.time else 'NO DATA'
    
    def __eq__(self,other) -> bool:
        if not isinstance(other, Lesson): return False
        if not self.course or not self.time: return False
        if not self.course or not other.time: return False
        return self.course == other.course and self.time == other.time

    def exists(self) -> bool:
        """
        Prüft, ob eine Stunde bereits vorhanden ist.

        :return: **True**, wenn die Stunde vorhanden ist
        """
        sql:str= 'SELECT * FROM lesson WHERE crs_name = ? AND les_time = ?'
        success:bool = False

        if not self.course or not self.time: return False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.course.name, self.db_time))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success

    def add(self) -> int:
        """
        Fügt eine Unterrichtstunde zur Datenbank hinzu.

        :return:
             | 0 - Erfolgreich
             | 1 - Zeitformat ungültig
             | 2 - Kurs nicht vorhanden
             | 3 - Stunde bereits vorhanden
        """

        if not self.time: return 1
        if not self.course: return 2

        students:list[tuple] = [(self.course.name, self.db_time, std.id) for std in self.course.students]
        sql:list[str] = [
            'INSERT INTO lesson VALUES(?,?,NULL)',
            'INSERT INTO lesson_student VALUES(?,?,?,false)'
        ]
        success:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql[0],(self.course.name, self.db_time))
                self.c.executemany(sql[1], students)
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3
    
    def remove(self) -> int:
        return 1
    
    def to_dict(self) -> dict[str,str]:
        return {}