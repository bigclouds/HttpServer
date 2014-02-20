import unittest
from uri_parser import map_uri

class TestMapUri(unittest.TestCase):
    """Test the uri mapping function. It should obtain a listing of the
    server's filesystem, check whether the file specified exists, and
    return the byte-representation of that file along with its mimetype
    code.
    """
