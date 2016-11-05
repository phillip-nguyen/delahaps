import sqlite3

dbfile = 'caldb.sqlite'

class CalDB:
    def __init__(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='EVENT'")
        if (not c.fetchall()):
            self.createTables()

    def connect(self):
        print 'connecting to database:', dbfile
        return sqlite3.connect(dbfile)
            
    def createTables(self):
        print "creating database:", dbfile
        conn = self.connect()
        c = conn.cursor()
        c.execute("""CREATE TABLE EVENT (
        id               INTEGER       PRIMARY KEY AUTOINCREMENT,
        created          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
        description      TEXT          Null,
        dtStart          DateTime      Null,
        dtEnd            DateTime      Null,
        geoLat           Float         Null,
        geoLng           Float         Null,
        lastModified     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
        organizerCN      TEXT          Null,
        organizerMailTo  TEXT          Null,
        summary          TEXT          Null,
        tags             TEXT          Null,
        title            TEXT          Null
        );""")
        conn.commit()
        conn.close()

    def addEvent(self, title, summary):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT INTO EVENT(title,summary) VALUES ('%s', '%s');" % (title, summary))
        conn.commit()
        conn.close()
        
    def list(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * from EVENT")
        allRows = c.fetchall()
        return allRows
        conn.close()
