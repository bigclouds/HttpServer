from email.utils import formatdate
from mimetypes import guess_type
import socket
from os.path import isfile, isdir
from os import listdir


def http_server():
    """Start an http server that listens for client requests."""
    #Set up the server socket.
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    try:
        #Connect the server socket.
        server_socket.bind(('127.0.0.1', 50000))
        server_socket.listen(1)

        #Loop indefinitely while waiting for connections.

        while True:
            try:
                conn, addr = server_socket.accept()
                msg = receive_message(conn)
                uri = parse_request(msg)
                resource, mimetype = map_uri(uri)

            except Error404:
                response = build_response(resource, mimetype, '404')

            except Error405:
                response = build_response(resource, mimetype, '405')

            except:
                response = build_response(resource, mimetype, '500')

            else:
                response = build_response(resource, mimetype)

            finally:
                conn.sendall(response)
                conn.shutdown(socket.SHUT_WR)
                conn.close()

    finally:
        #Make sure the socket is closed when we can't continue.
        print("Closing the socket.")
        server_socket.close()


def receive_message(conn, buffsize=4096):
    """When a connection is received by the http_server, this function
    pieces together the message received and returns it.
    """

    msg = ''
    while True:
        msg_part = conn.recv(buffsize)
        msg += msg_part
        if len(msg_part) < buffsize:
            break

    conn.shutdown(socket.SHUT_RD)

    return msg


def parse_request(request):
    first_rn = request.find('\r\n')
    first_line = request[:first_rn]
    if first_line.split()[0] == 'GET':
        uri = first_line.split()[1]
        return uri
    else:
        raise ParseException("405: Method not allowed. Only GET is allowed.")


def map_uri(uri):
    """Given a uri, looks up the corresponding file in the file system.
    Returns a tuple containing the byte-string represenation of its
    contents and its mimetype code.
    """
    #URIs come in based in root. Make root the 'webroot' directory.
    filepath = 'webroot' + uri

    if isfile(filepath):
        with open(filepath, 'rb') as infile:
            message = infile.readlines()

        return (message, guess_type(filepath)[0])

    if isdir(filepath):
        contents = listdir(filepath)
        return ('\n'.join(contents), 'text/plain')

    #If what we received was not a file or a directory, raise an Error404.
    raise Error404


def build_response(message, mimetype, code="OK 200"):
    """Build a response with the specified code and content."""

    if not isinstance(bytes):
        message = message.encode('utf-8')
    bytelen = len(bytes)
    header_list = []
    status_line = 'HTTP/1.1 ' + code + '\r\n'
    header_list.append(status_line)
    timestamp = 'Date: ' + formatdate(usegmt=True) + '\r\n'
    header_list.append(timestamp)
    server_line = 'Server: Team Python\r\n'
    header_list.append(server_line)
    content_type = 'Content-Type: ' + mimetype + '; char=UTF-8\r\n'
    header_list.append(content_type)
    content_len = 'Content-Length: ' + str(bytelen) + '\r\n'
    header_list.append(content_len)
    header_list.append('\r\n')
    header = '\r\n'.join(header_list)
    return (header, message)


class Error404(BaseException):
    """Exception raised when a file specified by a URI does not exist."""
    pass


class Error405(BaseException):
    """Exception raised when a method other than GET is requested."""
    pass


class ParseException(Exception):
    """An empty class to pass useful exceptions."""
    pass
