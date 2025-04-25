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
        self.__leader:Teacher|None = leader if isinstance(leader, Teacher) else None
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

    @property
    def leader(self) -> Teacher|None:
        """
        Verwaltet den Klassenleiter.

        :getter: Liefert den Klassenleiter
        :setter: Legt den Klassenleiter fest
        """
        return self.__leader
    
    @leader.setter
    def leader(self, leader:Teacher) -> None:
        sql:str = 'UPDATE grade SET teach_id = ? WHERE grd_name = ?'

        if isinstance(leader, Teacher) and leader.exists():
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(FKON)
                    self.c.execute(sql,(leader.id, self.name))
                    self.con.commit()
                    self.__leader = leader
            except Error as e: print(e)
            finally: self.close()

    def __repr__(self) -> str: return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Grade): return False
        return self.name == other.name

    def exists(self) -> bool:
        """
        Prüft, ob eine Klasse existiert.

        :return: **True**, wenn die Klasse bereits existiert
        """
        sql:str = 'SELECT * FROM grade WEHRE grd_name = ?'
        success:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql, (self.name,))
                res = self.c.fetchone()
                if res: success = True
        except Error as e: print(e)
        finally: self.close()

        return success

    def add(self) -> int:
        """
        Legt eine neue Klasse an.

        :return:
             | 0 - Erfolgreich
             | 2 - Der Klassenleiter existiert nicht
             | 3 - Klasse bereits vorhanden
        """
        sql:str = 'INSERT INTO grade VALUES(?,?)'
        success:bool = False

        if not isinstance(self.leader, Teacher) or not self.leader.exists(): return 2

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.name, self.leader.id))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3

    def remove(self) -> int:
        return 1
    
    def to_dict(self) -> dict[str,str]:
        return {}