from datetime import datetime
from database import DataObject, Course, Student, Error, FKON

class Lesson(DataObject):
    """
    Repräsentiert eine Unterrichstunde.

    :param course: Zugehöriger Kurs
    :param time: Geplanter Unterrichtsbeginn (JJJJ-TT-MM HH:MM)
    """
    def __init__(self, course:Course, time:str):
        course:Course|None = course if isinstance(course, Course) and course.exists() else None
        time:datetime|None = None

        try:
            time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        except ValueError as e: print(e)