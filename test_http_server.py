import unittest
import socket
from time import sleep
from os import listdir, fork, _exit
from http_server import Error404, Error405, map_uri, receive_message


class TestReceiveMessage(unittest.TestCase):
    """Test the receive_connection function, whose responsibility is to
    get the contents of a message being passed through a socket.
    """
    def setUp(self):
        self.empty_message = ''
        self.small_message = 'This message is small.'
        self.large_message = 'This message exceeds the buffer size.'
        self.exact_message = 'This message is 32 characters..'

    def test_empty_message(self):
        pid = fork()
        if pid:
            #Set up a dummy server socket to receive a connection from
            #the dummy client
            server = self.dummy_server()
            conn, addr = server.accept()

        else:
            self.dummy_client(self.empty_message)
            _exit(0)

        msg = receive_message(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        self.assertEqual(msg, self.empty_message)

    def test_message_below_buffer_size(self):
        pid = fork()
        if pid:
            #Set up a dummy server socket to receive a connection from
            #the dummy client
            server = self.dummy_server()
            conn, addr = server.accept()

        else:
            self.dummy_client(self.small_message)
            _exit(0)

        msg = receive_message(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        self.assertEqual(msg, self.small_message)

    def test_message_above_buffer_size(self):
        pid = fork()
        if pid:
            #Set up a dummy server socket to receive a connection from
            #the dummy client
            server = self.dummy_server()
            conn, addr = server.accept()

        else:
            self.dummy_client(self.large_message)
            _exit(0)

        msg = receive_message(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        self.assertEqual(msg, self.large_message)

    def test_message_exactly_buffer_size(self):
        pid = fork()
        if pid:
            #Set up a dummy server socket to receive a connection from
            #the dummy client
            server = self.dummy_server()
            conn, addr = server.accept()

        else:
            self.dummy_client(self.exact_message)
            _exit(0)

        msg = receive_message(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        self.assertEqual(msg, self.exact_message)

    def dummy_server(self):
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)

        sock.bind(('127.0.0.1', 50000))
        sock.listen(1)

        return sock

    def dummy_client(self, msg):
        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)

        client_socket.connect(('127.0.0.1', 50000))

        client_socket.sendall(msg)
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()


class TestParseRequestHeader(unittest.TestCase):
    """Test the parse_request_header function, which gets the command
    portion of the message header and parses for the request method and
    resource request.
    """
    pass


class TestMapUri(unittest.TestCase):
    """Test the uri mapping function. It should obtain a listing of the
    server's filesystem, check whether the file specified exists, and
    return the byte-representation of that file along with its mimetype
    code. These tests assume the use of the webroot directory provided
    in the assignment spec.
    """
    def setUp(self):
        self.directory_requested = '/images'
        self.image_requested = '/images/sample_1.png'
        self.text_requested = '/sample.txt'
        self.nonexistant_requested = '/iamnothere'

    def test_directory_requested(self):
        """Map a URI containing a request for a directory."""
        message, mimetype = map_uri(self.directory_requested)
        contents = listdir('webroot' + self.directory_requested)
        content_string = '\n'.join(contents)
        self.assertEqual(message, content_string)
        self.assertEqual(mimetype, 'text/plain')

    def test_image_file_requested(self):
        """Map a URI containing a request for an image file."""
        message, mimetype = map_uri(self.image_requested)

        with open('webroot' + self.image_requested, 'rb') as infile:
            expected = infile.readlines()

        self.assertEqual(message, expected)
        self.assertEqual(mimetype, 'image/png')

    def test_text_file_requested(self):
        """Map a URI containing a request for a text file."""
        message, mimetype = map_uri(self.text_requested)

        with open('webroot' + self.text_requested, 'rb') as infile:
            expected = infile.readlines()

        self.assertEqual(message, expected)
        self.assertEqual(mimetype, 'text/plain')

    def test_nonexistent_resource_requested(self):
        """Map a URI containing a request for a resource that doesn't
        exist.
        """
        self.assertRaises(Error404, map_uri, self.nonexistant_requested)


class TestBuildResponse(unittest.TestCase):
    """Test build_response by attempting to build a proper message given
    the correct resources.
    """
    pass


if __name__ == '__main__':
    unittest.main()
