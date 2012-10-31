import functools
import re

import tornado.web
import utils

class DocHandler(tornado.web.RequestHandler):
    """
    Automatically outputs documentation for the applications handlers
    using the docstring of each handler.
    """
    @staticmethod
    def _get_helper(application,
        handlers=None,
        server_name=None,
        request=None,
        ):
        """
        @param handlers: list(RequestHandler), list of handlers to limit
        the documentation for. If not specified, documentation will be
        generated for all handlers.
        @param server_name: str, will be used as the title in the generated
        HTML.
        @param request: HTTPRequest|None
        @return: str
        """
        urls = application.handlers[0][1]
        classes = [h.__class__ for h in handlers] if handlers else None
        server_name = server_name or application.settings.get('server_name', "")
        endpoints = []
        request_path = request.path if request else ''
        request_query = request.query if request else ''
        for url in urls:
            if classes and not url.handler_class in classes:
                continue
            if url.handler_class.__module__.startswith('tornado.'):
                continue
            if url.handler_class.__name__ == DocHandler.__name__:
                continue
            path = url.regex.pattern.replace('$', '').replace('.*?', '')
            path = re.sub(r'^/', r'', path)
            endpoint = utils.Endpoint(url.handler_class.__doc__, path)
            endpoints.append(endpoint)
        return utils.get_api_doc(endpoints, server_name,
                request_path=request_path,
                request_query=request_query,
                )

    def get(self, classses=None):
        self.write(self._get_helper(self.application, request=self.request))

class document(object):
    """
    Decorator to add to the tornado get method to get documentation out
    of it.
    """
    def __init__(self, param='doc'):
        """
        @param param: str|None, if param in the url request, return
        documentation. Otherwise, go with the normal get method. If param=None
        return documentation if there are no parameters in the request.
        """
        self._param = param

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapped_f(*args, **kwargs):
            handler = args[0]
            if ((self._param and handler.get_argument(self._param, None)) or
                    (not self._param and not handler.request.arguments)):
                server_name = None
                if hasattr(handler, 'get_server_name'):
                    server_name = handler.get_server_name()
                handler.write(DocHandler._get_helper(handler.application,
                    handlers=[handler],
                    server_name=server_name,
                    request=handler.request,
                    ))
                return
            return fn(*args, **kwargs)
        return wrapped_f
