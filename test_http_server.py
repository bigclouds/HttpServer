import unittest
import http_server


class TestReceiveConnection(unittest.TestCase):
    """Test the receive_connection function, whose responsibility is to
    get the contents of a message being passed through a socket.
    """
    pass


class TestParseRequestHeader(unittest.TestCase):
    """Test the parse_request_header function, which gets the command
    portion of the message header and parses for the request method and
    resource request.
    """
    pass


class TestMapUri(unittest.TestCase):
    """Test map_uri, which maps the URI of the request onto the filesystem."""
    pass


class TestBuildResponse(unittest.TestCase):
    """Test build_response by attempting to build a proper message given
    the correct resources.
    """
    pass


if __name__ == '__main__':
    unittest.main()
