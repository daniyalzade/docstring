import re
import urllib
from urlparse import urlparse
from urlparse import urlunparse

def _parse_params(url):
    """
    Given a url, return params as dict

    @param url: str
    @return dict(str,str)
    """
    url_parts = list(urlparse(url))
    params = (dict([part.split('=') for part in url_parts[4].split('&')]) if
             url_parts[4] else {})
    return params

def _append_params(url, params):
    """
    Append parameters to an existing url. The appended parameters will be
    properly urlencoded. It wont append a parameter if it already exists

    Ideally, params should be list of tuples, but the method accepts dict
    for legacy reasons.

    @param url: str
    @param params: dict(str,str)|list(tuple), parameters to append
    @return str: url with the parameters appended
    """
    assert(isinstance(params, dict) or isinstance(params, list))

    if isinstance(params, dict):
        params = params.items()

    url_parts = list(urlparse(url))
    query = ([part.split('=') for part in url_parts[4].split('&')] if
             url_parts[4] else [])
    params = query + params
    to_append = []
    for key, value in params:
        if type(value) == unicode:
            value = value.encode('utf-8')

        if not key in [k for (k, v) in to_append]:
            to_append.append((key, value))

    url_parts[4] = urllib.urlencode(to_append)
    to_return = urlunparse(url_parts)
    return to_return

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
    def __init__(self, docstring, mount_regex):
        """
        @param pydoc: str
        @param path: str
        """
        self._docstring = docstring
        self._mount_regex = mount_regex

    def _get_path(self, request_path=None, clean=False, params={}):
        """
        @param path: str
        @param clean: bool
        @param params: dict
        """
        path = self._mount_regex.replace('$', '').replace('.*?', '')
        path = re.sub(r'^/', r'', path)
        if not clean:
            path = _append_params(path, params)
        return path

    def get_link_path(self, request_path, clean=False, params={}):
        """
        @param request_path: str
        @return: str
        """
        params['doc'] = 1
        link_path = self._get_path(
                request_path=request_path,
                clean=clean,
                params=params,
                )
        print link_path
        return link_path

    def get_display_path(self, request_path, clean=False, params={}):
        """
        @param request_path: str
        @return: str
        """
        display_path = self._get_path(
                request_path=request_path,
                clean=clean,
                params=params,
                )
        print display_path
        return display_path

    def get_doc(self, request_path):
        """
        @param request_path: str
        @return: str
        """
        if not self._docstring:
            return ""
        docstring = self._docstring.strip()
        link_path = self.get_link_path(request_path, clean=False)
        display_path = self.get_display_path(request_path, clean=False)
        print link_path, display_path, 'in doc'
        doc = ""
        doc = docstring.replace('\n', '<br/>\n')
        doc = re.sub(r'@param ([^:]+):', r'<span class="param">\1</span>:', doc)
        doc = re.sub(r'@see: ([^\n]+)<br/>', r"<span class='link'><a href='%s\1'>%s\1</a></span><br/>" % (link_path, display_path), doc)
        return doc

def get_api_doc(endpoints, title, request_url, doc_param=None):
    """
    @param endpoints: list(Endpoint)
    @param title: str
    @param request_url: path
    @return: str
    """
    request_params = _parse_params(request_url)
    request_path = urlparse(request_url)[2]
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
        link_path = endpoint.get_link_path(
                request_path,
                params=request_params,
                )
        display_path = endpoint.get_display_path(request_path)
        docs = endpoint.get_doc(request_path)
        out.append('<td><a href="%s">%s</a></td>' % (link_path, display_path))
        out.append('<td>%s</td>' % docs)
        out.append('</tr>')
    out.append('</tbody>')
    out.append('</body>')
    out.append('</html>')
    return ('\n'.join(out))

