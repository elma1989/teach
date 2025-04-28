from datetime import datetime
from database import DataObject, Course, Student, Error, FKON

class Lesson(DataObject):
    """
    Repräsentiert eine Unterrichstunde.

    :param course: Zugehöriger Kurs
    :param time: Geplanter Unterrichtsbeginn (JJJJ-TT-MM HH:MM)
    """
    def __init__(self, course:Course, time:str, topic:str = '') -> None:
        self.__course:Course|None = course if isinstance(course, Course) and course.exists() else None
        self.__time:datetime|None = None
        self.__topic:str = topic
        self.__homeworks:list[str] = []
        self.__students:list[tuple[Student,bool]] = []

        try:
            time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        except ValueError as e: print(e)

    @property
    def course(self) -> Course|None:
        ''':getter: Liefert den aktuellen Kurs'''
        return self.__course
    
    @property
    def time(self) -> datetime|None:
        """
        Verwaltet den Unterrichtsbegin.

        :getter: Liefert den Unterrichtsbegin
        :setter: Ändert den Unterrichtsbegin (JJJJ-MM-TT HH:MM)
        :return: datetime-Objekt des Unterrichtsbegins
        """
        return self.__time
    
    @property
    def db_time(self) -> str:
        """
        :getter: Liefert die Datenbankzeit der Stunde
        :return: Zeit (JJJJ-MM-TT HH:MM)
        """
        return self.time.strftime('%Y-%m-%d %H:%M') if self.time else ''
    
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
        sql:str = 'UPDATE lesson SET les_topic = ?'

        if self.course and self.time:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(topic,))
                    self.con.commit()
            except Error as e: print(e)
            finally: self.close()