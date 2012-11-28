import unittest

from docstring.utils import Endpoint

doc = """
    Return list of spikes for given host

    Examples:
    @see: ?start=10m&end=1m&host=nytimes.com

    @param host: str
    @param _id: int, spike id
    @param start: str|None, values: unix_ts, 5m, 10h, YYYY-mm-dd, HH:MM:SS, [default: 10m]
    @param end: str|None, values: unix_ts, YYYY-mm-dd, YYYY-mm-dd, HH:MM:SS, [default: 1m]
    @param limit: int|None, number of spikes to return. If provided, we ignore
    the start|end.
    @param human: bool|None
"""
class TestEndpoint(unittest.TestCase):
    def test_base_endpoint(self):
        endpoint = Endpoint(doc, '/hello/')
        self.assertEquals('./hello/?foo=bar', endpoint.get_link_path(
                request_path='/',
                params={'foo': 'bar'},
                ))
        self.assertEquals('./hello/', endpoint.get_display_path(
                request_path='/',
                ))

    def test_api_endpoint(self):
        endpoint = Endpoint(doc, '/hello/')
        self.assertEquals('./?foo=bar', endpoint.get_link_path(
                request_path='/hello/',
                params={'foo': 'bar'},
                ))
        self.assertEquals('./', endpoint.get_display_path(
                request_path='/hello/',
                ))

    def test_mounted_base_endpoint(self):
        endpoint = Endpoint(doc, '/hello/')
        self.assertEquals('./hello/?foo=bar', endpoint.get_link_path(
                request_path='/mount/path/',
                params={'foo': 'bar'},
                ))
        self.assertEquals('./hello/', endpoint.get_display_path(
                request_path='/mount/path/',
                ))

    def test_get_description(self):
        endpoint = Endpoint(doc, '/hello/')
        description = endpoint.get_description()
        self.assertEquals(
                'Return list of spikes for given host',
                description,
                )

    def test_get_params(self):
        endpoint = Endpoint(doc, '/hello/')
        params = endpoint.get_params()
        print params


if __name__ == "__main__":
    unittest.main()

