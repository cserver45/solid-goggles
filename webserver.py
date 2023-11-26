"""webserver.py - A simple script using cherrypy just here to host the feed.rss all the time"""
import os
import cherrypy

# server configuration
cherrypy.config.update({'server.socket_port': 8976, "server.socket_host": "0.0.0.0"})

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Well Hello There..."

if __name__ == '__main__':
   cherrypy.quickstart(Root(), '/', {"/feed.rss": {"tools.staticfile.on": True, "tools.staticfile.filename": f"{os.getcwd()}/feed.rss"}})