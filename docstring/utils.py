import re
from urlparse import urlparse
from urlparse import urlunparse

class Pydoc(object):
    def __init__(self, docstring):
        """
        @param docstring: str
        """
        self._docstring = docstring

    def to_html(self):
        pass

    def remove_all(self, params):
        """
        @param params: list(str)
        @return: Pydoc
        """
        for param in params:
            pattern = r"@param %s: .*?@param" % param
            # Do a multiline match (re.M) and do not treat \n as a special
            # character (re.S)
            pattern = re.compile(pattern, flags=re.M|re.S)
            self._docstring = re.sub(pattern, '@param', self._docstring)
            # Unfortunate hack to handle @param being the last line
            pattern = r"@param %s: .*" % param
            pattern = re.compile(pattern, flags=re.M|re.S)
            self._docstring = re.sub(pattern, '', self._docstring)
        return self

    def remove(self, param):
        """
        @param params: str
        @return: Pydoc
        """
        return self.remove_all([param])

    def to_docstring(self):
        return self._docstring

class Endpoint(object):
    def __init__(self, pydoc, path):
        self.pydoc = pydoc
        self.path = path

def _get_endpoint_doc(endpoint, request_path):
    """
    @param endpoint: Endpoint
    @param request_path: str
    @return: str
    """
    path = endpoint.path
    pydoc = endpoint.pydoc
    if not pydoc:
      return ""
    pydoc = pydoc.strip()
    # Make sure that we only use relative paths
    path = re.sub(r'^/', r'', path)

    path_to_append = '' if request_path else path
    doc = ""
    doc = pydoc.replace('\n', '<br/>\n')
    doc = re.sub(r'@param ([^:]+):', r'<span class="param">\1</span>:', doc)
    doc = re.sub(r'@see: ([^\n]+)<br/>', r"<span class='link'><a href='%s\1'>%s\1</a></span><br/>" % (path_to_append, path), doc)
    return doc

def get_api_doc(endpoints, title, request_path='', request_query=''):
    """
    @param endpoints: list(Endpoint)
    @param title: str
    @param request_path: str
    @param request_query: str, e.g. doc=1, this will get appended to paths for
    on different api endpoints
    @return: str
    """
    out = []
    out.append('<html>')
    out.append('<head>')
    out.append('  <title>%s</title>' % title)
    out.append(""" <style type="text/css">
    .param {
        font-weight: bold;
        margin-right: 20px;
    }
    .link {
        margin-left: 20px;
    }
    </style>""")
    out.append('<link href="http://twitter.github.com/bootstrap/assets/css/bootstrap.css" rel="stylesheet">')
    out.append('</head>')
    out.append('<body>')
    if title:
        out.append('<h2>%s</h2>' % title)
    out.append('<table class="table table-bordered table-striped">')
    out.append('<thead>')
    out.append('<tr>')
    out.append('<th>url</th>')
    out.append('<th>description</th>')
    out.append('</tr>')
    out.append('</thead>')
    out.append('<tbody>')
    for endpoint in endpoints:
        path = endpoint.path
        # Make sure that we only use relative paths
        path = re.sub(r'^/', r'', path)
        # If there were query parameters, append them to the URL to the API
        # endpoint. This is needed where we have doc=1 or another paramter to
        # signify returning the docstring. We should propagate that to the
        # endpoints.
        if request_query:
            parts = urlparse(path)
            parts = [p for p in parts]
            parts[4] = parts[4] + request_query
            path = urlunparse(parts)
        docs = _get_endpoint_doc(endpoint, request_path)
        out.append('<td><a href="%s">%s</a></td>' % (path, path))
        out.append('<td>%s</td>' % docs)
        out.append('</tr>')
    out.append('</tbody>')
    out.append('</body>')
    out.append('</html>')
    return ('\n'.join(out))

