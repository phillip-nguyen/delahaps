import cherrypy, datetime
import caldb

class Root(object):        
    @cherrypy.expose
    def index(self):
        return open('index.html');

    @cherrypy.expose
    def addevent(self):
        return open('addevent.html');
        

class Events(object):
    exposed = True
    
    def __init__(self):
        self.calendar = caldb.CalDB()

    def GET(self, action=None, **params):
        if action == 'query':
            return '<p>\n'.join(map(self.calendar.htmlForEvent, self.calendar.queryEvents(params)))
        else:
            return '<p>\n'.join(map(self.calendar.htmlForEvent, self.calendar.list()))
        

class Uploader(object):
    exposed = True

    def __init__(self):
        self.calendar = caldb.CalDB()
    
    def POST(self, title=None, summary=None, category=None, description=None, date=None):
        if title and summary:
            print "date = ", date
            m, d, y = map(int, date.split('/'))
            date = datetime.date(y, m, d)
            self.calendar.addEvent(title, summary, category, description, date)
        raise cherrypy.HTTPRedirect("/")
    
if __name__ == '__main__':
    #cherrypy.quickstart(Root(), '/')
    cherrypy.tree.mount(Root(), '/')
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

    
