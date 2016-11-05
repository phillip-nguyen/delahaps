import cherrypy
import caldb

class Root(object):
    def __init__(self):
        self.calendar = caldb.CalDB()
        
    @cherrypy.expose
    def index(self):
        return '<br>\n'.join(map(str, self.calendar.list()))

class Events(object):
    exposed = True
    
    def __init__(self):
        self.calendar = caldb.CalDB()

    def GET(self, theID=None):
        if not theID:
            return '<br>\n'.join(map(str, self.calendar.list()))
        else:
            return str(self.calendar.getEventWithID(theID))

class Uploader(object):
    exposed = True

    def __init__(self):
        self.calendar = caldb.CalDB()
    
    def POST(self, title=None, summary=None):
        if not title or not summary:
            return "missing data"
        self.calendar.addEvent(title, summary)
        return "Added new event!"
    
if __name__ == '__main__':
    cherrypy.tree.mount(
        Events(), '/events',
        {'/': {'request.dispatch':cherrypy.dispatch.MethodDispatcher()}}
    )
    cherrypy.tree.mount(
        Uploader(), '/add',
        {'/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on':True,
            'tools.response_headers.headers':[('Content-Type', 'text/plain')],
            
        }}
    )
        
    cherrypy.engine.start()
    cherrypy.engine.block()
    #cherrypy.quickstart(Root(), '/')
    
