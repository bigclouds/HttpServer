from mimetypes import guess_type
from os.path import isfile, isdir
from os import listdir


class Error404(BaseException):
    """Exception raised when a file specified by a URI does not exist."""
    pass


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
        return (u'\n'.join(contents).encode('utf-8'), 'text/plain')

    #If what we received was not a file or a directory, raise an Error404.
    raise Error404
