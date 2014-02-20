from mimetypes import guess_type


class Error404(BaseException):
    """Exception raised when a file specified by a URI does not exist."""
    pass


def map_uri(uri):
    """Given a uri, looks up the corresponding file in the file system.
    Returns a tuple containing the byte-string represenation of its
    contents and its mimetype code.
    """
    pass
