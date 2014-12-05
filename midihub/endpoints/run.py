import json
import os
import subprocess


class ProcRunner(object):
    def __init__(self, arg):
        if '/' not in arg and os.path.isfile(arg) and os.access(arg, os.X_OK):
            arg = './' + arg
        self.proc = subprocess.Popen([arg], stdin=subprocess.PIPE)

    def emit(self, code, *args):
        try:
            self.proc.stdin.write(json.dumps([code] + list(args)) + '\n')
        except IOError:
            if self.proc.poll() is 0:
                raise StopIteration()
            else:
                raise

    def eof(self):
        self.proc.stdin.close()


make_dst = ProcRunner
