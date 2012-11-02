import tornado.ioloop
import tornado.web

from docstring.tornadodoc import DocHandler
from docstring.tornadodoc import document

class ByeHandler(tornado.web.RequestHandler):
    """
    Returns a 'bye <name>' response.

    @param name: str, [default: 'foo']
    """

    @document()
    def get(self):
        name = self.get_argument('name', 'foo')
        self.write("Bye %s" % name)

class HelloHandler(tornado.web.RequestHandler):
    """
    Returns a 'hello <name>' response.

    @param name: str, [default: 'foo']
    """

    @document()
    def get(self):
        name = self.get_argument('name', 'foo')
        self.write("Hello %s" % name)

application = tornado.web.Application([
    (r"/hello", HelloHandler),
    (r"/bye", ByeHandler),
    (r"/", DocHandler),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
