from database import DataObject, Teacher, Error, FKON

class Grade(DataObject):
    """
    Repräsentiert eine Schulklasse.

    :param name: Name der Klasse
    :param leader: Lehrer-Instanz, des Klassenleiters

    .. note:: Es ist zu emphehlen, dass bei jährlich wechselden Klassennamen die Klassenstufen unter 10 mit einer führenden 0 
        z. B. 09a zu beginnen, da eine alphabetische Soritierung bei Klassenlisten vorgenommen wird.
    """
    def __init__(self, name:str, leader:Teacher|None = None) -> None:
        super().__init__()
        self.__name:str = name
        self.__leader:Teacher|None = None
        sql:str = """SELECT t.teach_first_name, t.teach_last_name, t.teach_birth_date, t.teach_id
            FROM teacher.t JOIN grade g
            WHERE g.grd_name = ?"""
        
        if not leader:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(name,))
                    res = self.c.fetchone()
                    if res: self.__leader = Teacher(res[0],res[1],res[2],res[3])
            except Error as e: print(e)
    
    @property
    def name(self) -> str:
        """
        Verwatet den Klassennamen.

        :getter: Liefert den Namen der Klasse
        :setter: Ändert den Klassennamen
        """
        return self.__name
    
    @name.setter
    def name(self,name:str) -> None:
        sql:str = """UPDADE grade
            SET grd_name = ?
            WHERE grd_name = ?"""
        
        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql, (name, self.name))
                self.con.commit()
        except Error as e: print(e)
        finally: self.close()