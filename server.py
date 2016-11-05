import cherrypy
import caldb

class Root(object):
    def __init__(self):
        self.calendar = caldb.CalDB()
        
    @cherrypy.expose
    def index(self):
        return '<br>\n'.join(map(str, self.calendar.list()))

if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/')
    
