from email.utils import formatdate
from mimetypes import guess_type
from socket import socket


def http_server():
    """Start an http server that listens for client requests."""
    pass


def receive_connection():
    """When a connection is received by the http_server, this function
    processes the connection and returns the message contents.
    """
    pass


def parse_request_header(header):
    """Parse the command line from the HTTP header."""
    pass


def map_uri(uri):
    pass


def build_response(code, contents):
    """Build a response with the specified code and content."""
    pass
