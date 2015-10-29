
class FileIterWrapper(object):
    """
    Python's default read() implementation reads byte-by-byte until it finds a
    newline. Video files are binary, so it could potentially be a long time until
    a newline or EOF is found. Instead, this reads from a file in 1mb chunks
    """
    def __init__(self, flo, chunk_size = 1024**2):
        self.flo = flo
        self.chunk_size = chunk_size

    def next(self):
        data = self.flo.read(self.chunk_size)
        if data:
            return data
        else:
            raise StopIteration

    def __iter__(self):
        return self
