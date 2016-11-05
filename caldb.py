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
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * from EVENT")
        allRows = c.fetchall()
        conn.close()
        return allRows

    def getEventWithID(self, theID):
        conn = self.connect()
        conn.row_factory = sqlite3.Row        
        c = conn.cursor()
        c.execute("SELECT * from EVENT WHERE id=%s" % theID)
        row = c.fetchone()
        conn.close()
        return row

    def queryEvents(self, where):
        conn = self.connect()
        conn.row_factory = sqlite3.Row        
        c = conn.cursor()
        s = "SELECT * from EVENT WHERE "
        s += ' AND '.join(["%s='%s'" % (x, where[x]) for x in where])
        c.execute(s)
        rows = c.fetchall()
        conn.close()
        return rows

    def dumpEvent(self, row):
        s = ''
        for x in row.keys():
            s += "%s : %s<br>\n" % (x, row[x])
        return s

    def htmlForEvent(self, row):
        s = ''
        s += '<div class="event">'
        s += row['title'] + '</br>'
        s += row['summary']
        s += '</div>'
        return s
    
