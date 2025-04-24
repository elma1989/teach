from sqlite3 import Error
import os

FKON = 'PRAGMA foreign_keys = ON'
DBPATH = '../teach.db'

from .data import Data, DataObject
from .subject import Subject
from .person import Person
from .school import School

def indb():
    """
    Initialisiert die Datenbank.

    .. important:: Die gasamte Datenbank wird dabei durch eine neue ersetzt. 
        Diese Funktion wird auch in Pytests verwendet. Sobald reale Daten existieren, sollten keine Pytests mehr durchgführt werden.
    """
    TABLEPATH = 'database/tables.sql'
    global DBPATH
    data = Data()

    if os.path.exists(DBPATH): os.remove(DBPATH)

    if os.path.exists(TABLEPATH):
        with open(TABLEPATH, 'r') as f:
            sql = f.read()

        try:
            data.connect()
            if data.con:
                data.con.executescript(sql)
        except Error as e: print(e)
        finally: data.close()