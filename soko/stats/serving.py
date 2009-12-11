
from StringIO import StringIO
import logging
import os.path

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def make_server(port):
    """Creates a simple local server.
    It serves files and output from .py scripts.
    """
    server = HTTPServer(("localhost", port), RequestHandler)
    logging.info("Listening on port %s", port)
    server.serve_forever()

class RequestHandler(SimpleHTTPRequestHandler): 
    def send_head(self):
        if _is_script(self.path):
            return self._send_script_output()
        else:
            return SimpleHTTPRequestHandler.send_head(self)

    def _send_script_output(self):
        args = ["./" + self.path[1:]]
        output = _capture_output(args)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(output))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        return StringIO(output)

def _is_script(path):
    return path.endswith(".py")

def _capture_output(cmd_args):
    import subprocess
    logging.info("Starting process: %s", cmd_args)
    process = subprocess.Popen(cmd_args, bufsize=-1,
            stdout=subprocess.PIPE, close_fds=True)

    output = process.stdout.read()
    returncode = process.wait()
    if returncode != 0:
        raise OSError("Process %s exited with code: %s" %
                (cmd_args, returncode))

    return output

