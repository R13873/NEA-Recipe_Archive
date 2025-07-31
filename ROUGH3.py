import sqlite3
import os

def createTables():
    cur.executescript(
        """CREATE TABLE test (
id INT(4) PRIMARY KEY,
string TEXT NOT NULL);
""")
    #executescript() allows you to execute multiple SQL statements in one call
    conn.comit()
    #adds result tof the execute into the database
    #NOT NULL prevents you from creating a new record without a value in this field
    #FOREIGN KEY(<field_name>) REFERENCES <table_name>(<primary_key>)

if not os.path.exists("test.db"):
    #checks if database exists, then connects
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    createTables()
else:
    #creates new database
    conn = sqlite3.connect("test.db")
    conn.cursor()

