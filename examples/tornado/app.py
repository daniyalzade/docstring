import tornado.ioloop
import tornado.web

from docstring.tornadodoc import DocHandler
from docstring.tornadodoc import document

class _NameHandler(tornado.web.RequestHandler):
    def _get_name(self):
        first = self.get_argument('first', 'foo')
        last = self.get_argument('last', 'bar')
        return first + " " + last

class ByeHandler(_NameHandler):
    """
    Returns a 'bye <first> <last>' response.

    @see: ?first=eytan&last=daniyalzade

    @param first: str, [default: 'foo']
    @param last: str, [default: 'foo']
    """
    @document(server_name='Bye Endpoint')
    def get(self):
        name = self._get_name()
        self.write("Bye %s" % name)

class HelloHandler(_NameHandler):
    """
    Returns a 'hello <first> <last>' response.

    @see: ?first=eytan&last=daniyalzade

    @param first: str, [default: 'foo']
    @param last: str, [default: 'foo']
    """
    @document(server_name='Hello Endpoint')
    def get(self):
        name = self._get_name()
        self.write("Hello %s" % name)

class OtherHandler(tornado.web.RequestHandler):
    """
    Returns a 404ish response
    """
    def get(self):
        self.write("This is not what you are looking for! 404!")

application = tornado.web.Application([
    (r"/hello/.*", HelloHandler),
    (r"/bye/.*", ByeHandler),
    (r"/.+", OtherHandler),
    (r"/", DocHandler, {'server_name': 'My Name Server'}),
], debug=True)

if __name__ == "__main__":
    port = 8888
    print "listening to %s" % port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
