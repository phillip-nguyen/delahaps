import sqlite3
import datetime
from icalendar import Calendar, Event

dbfile = 'caldb.sqlite'

Date = datetime.date

class CalDB:
    def __init__(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='EVENT'")
        if (not c.fetchall()):
            self.createTables()
            self.populate()            

    def connect(self):
        print 'connecting to database:', dbfile
        return sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
            
    def createTables(self):
        print "creating database:", dbfile
        conn = self.connect()
        c = conn.cursor()
        c.execute("""CREATE TABLE EVENT (
        id               INTEGER       PRIMARY KEY AUTOINCREMENT,
        category         TEXT          Null,
        created          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
        description      TEXT          Null,
        dtStart          TIMESTAMP     Null,
        dtEnd            TIMESTAMP     Null,
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

    def addEvent(self, title, summary, category, description, date):
        conn = self.connect()
        c = conn.cursor()
        date = datetime.datetime.combine(date, datetime.time())
        c.execute("INSERT INTO EVENT(title,summary,category,description,dtStart) VALUES (?, ?, ?, ?, ?)", (title, summary, category, description, date))
        conn.commit()
        conn.close()

    def populate(self):
        self.addEvent('Chicken Roulette', 'You might win a random chicken!', 'arts', 'Second Annual Chicken Roulette Festival', Date(2016, 11, 4))
        self.addEvent('OpenBracket', 'Coding Competition', 'volunteer', 'A contest for programmers in Delaware', Date(2016,11,4))
        self.addEvent('Adult Dog Classes', 'Old dogs can learn new tricks', 'education', 'Free magic classes for older dogs', Date(2016,12,25))
        self.addEvent('Folk Music Festival', 'Your favorite folk bands', 'music', 'blah', Date(2016,11,10))
        self.addEvent('Michael Jordan Sings', 'From basketball to crooning', 'music', 'blah', Date(2016,11,1))
        self.addEvent('Wine Tasting', 'What does wine taste like? Find out!', 'food', 'blah', Date(2016,11,5))
        
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
        if 'dtStart' in where:
            m,d,y = map(int, where['dtStart'].split('-'))
            date = datetime.datetime.combine(Date(y,m,d), datetime.time())
            where['dtStart'] = str(date)
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
        s += '<b>' + row['title'] + '</b></br>'
        s += row['summary'] + '</br>'
        s += str(row['dtStart']).split()[0] + '</br>'
        s += '<i>' + row['category'] + '</i>'
        s += '</div>'
        return s
    
    def icalForEvent(self, row):
        cal = Event()
        cal['title'] = row['title']
        cal['summary'] = row['summary']
        cal['description'] = row['description']
        cal.add('dtstart', row['dtStart'])
        return cal.to_ical().replace('\r\n', '\n').strip()
