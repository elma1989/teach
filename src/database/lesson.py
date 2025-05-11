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
        return self.time.strftime('%Y-%m-%d %H:%M') if self.time else '-'

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
        sql:str = """UPDATE lesson SET les_time = ?
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
            except ValueError as f:print(f)
            finally: self.close()

    @property
    def topic(self) -> str:
        """
        Vervaltet das Thema der Stunde.

        :getter: Liefert das Thema
        :setter: Legt des Thema fest
        """
        sql:str = 'SELECT les_topic FROM lesson WHERE crs_name = ? AND les_time = ?'

        if self.exists() and len(self.__topic) == 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql, (self.course.name, self.db_time))
                    res = self.c.fetchone()
                    if res and res[0]: self.__topic = res[0]
            except Error as e: print(e)
            finally: self.close()
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
            WHERE crs_name = ? AND les_time = ? ORDER BY les_homework"""
        
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
        """
        :getter: Liefert eine Liste der Studenten und dem Anwensenheitsstatus
        :return: Eine Liste aus Tupeln mit der Instanz des Schülers und einem boolischen Wert (**True** = anwesend)
        """
        sql:str = """SELECT s.std_first_name, s.std_last_name, s.std_birth_date, s.std_id, ls.les_student_present
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
        """
        Löscht eine Stunde.

        :return:
             | 0 - Erfolgreich
             | 1 - Stunde nicht vorhanden
        """
        sql:str = 'DELETE FROM lesson WHERE crs_name = ? AND les_time = ?'
        success:bool = False

        if not self.course or not self.time: return 1
        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.course.name, self.db_time))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1

    
    def to_dict(self) -> dict[str,str]:
        """
        Liefert die Kerndaten einer Stunde für weiter Anfragen

        :return: Wörterbuch der Stunde
        """
        return {
            'course':self.course.name if self.course else '-',
            'time':self.db_time,
            'topic':self.topic
        }

    def add_homework(self, task:str) -> int:
        """
        Legt eine neue Hausaufabe an.

        :param task: Zu erlegigende Aufgabe
        :return:
             | 0 - Erfolgreich
             | 1 - Stunde wurde nicht gefunden
             | 2 - Hausaufgabe bereits eingetragen
        """
        sql:str = 'INSERT INTO lesson_homework VALUES(?,?,?)'
        success:bool = False

        if not self.course or not self.time: return 1
        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql, (self.course.name, self.db_time, task))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 2

    def set_present_status(self, presents:list[bool]) -> int:
        """
        Spreichert die zutreffenden Anwesenheitsstati ab.

        :param presents: Liste mit Anwesenheitsstati (**True** = anwesend) in identischer Reihenfolge der Liste der Kursteilnehmer
        :return:
             | 0 - Erfolgreich
             | 1 - Übermittelte Liste ist nicht korekt
             | 2 - Stunde wurde nicht gefunden
        """
        sql:str = """UPDATE lesson_student SET les_student_present = ?
            WHERE crs_name = ? AND les_time = ? AND std_id = ?"""
        success:bool = False
        
        if not self.course or not self.time: return 2
        if not self.exists(): return 2
        if len(self.course.students) != len(presents): return 1
        for case in presents:
            if type(case) != bool: return 1
        
        data:list[tuple] = [(y, self.course.name, self.db_time, x.id) for x,y in zip(self.course.students, presents)]

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.executemany(sql, data)
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1