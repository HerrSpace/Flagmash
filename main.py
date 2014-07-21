import sys
import os

import cherrypy

from flag_app.PageHandler import Root

if __name__ == '__main__':
	ip = '127.0.0.1'
	port = 8081
	static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

	cherrypy.config.update({'server.socket_host': ip})
	cherrypy.config.update({'server.socket_port': port})

	example_controller = Root(ip, port)

	d = cherrypy.dispatch.RoutesDispatcher()
	d.connect(name='root',		action='index',		controller=example_controller,	route='/')
	d.connect(name='root',		action='index_r',	controller=example_controller,	route='/:game/:winner')
	d.connect(name='root',		action='stats',	controller=example_controller,	route='/stats')	

	config_dict = {
		'/': {
			'request.dispatch': d,
			'tools.staticdir.on': False,
			'tools.staticdir.root': static_root,
			'tools.staticdir.dir': '.',
			'request.show_tracebacks': False
		}
	}

	cherrypy.tree.mount(None, config=config_dict)
	cherrypy.engine.start()
	cherrypy.engine.block()
