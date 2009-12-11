
import os
import errno
import gzip

def _store_atomic_data(path, data):
    prepare_path(path)
    tmppath = path + ".tmp"
    if path.endswith(".gz"):
        output = gzip.GzipFile(tmppath, "wb")
    else:
        output = file(tmppath, "wb")
    output.write(data)
    output.flush()
    os.fsync(output.fileno())
    output.close()
    os.rename(tmppath, path)

def prepare_path(path):
    head, tail = os.path.split(path)
    if len(head) == 0:
        return
    try:
        os.makedirs(head)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def open(path):
    if path.endswith(".gz"):
        output = gzip.GzipFile(path)
    else:
        output = file(path)
    return output

def store_content(path, content):
    data = content
    if isinstance(content, unicode):
        data = content.encode("utf-8")
    _store_atomic_data(path, data)

