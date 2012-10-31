import unittest

from docstring.utils import Pydoc

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
class TestUrlUtils(unittest.TestCase):
    def test_pydoc(self):
        pydoc = Pydoc(doc)
        pydoc.remove_all(['_id', 'human'])
        docstring = pydoc.to_docstring()
        self.assertTrue(not 'human' in docstring)
        self.assertTrue(not '_id' in docstring)

if __name__ == "__main__":
    unittest.main()

