from database import DataObject, Teacher, Subject, Error, FKON

class Course(DataObject):
    """
    Respäsentiert einen Kurs.

    :param name: Kursname
    :param leader: Lehrerinstanz des Klassenleiters (Standard: None)
    :param subject: Instanz des Faches (Standard: None)
    """
    def __init__(self, name:str, leader:Teacher|None=None, subject:Subject|None=None):
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