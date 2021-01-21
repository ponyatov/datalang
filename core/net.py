from .io import *
from .number import *

import re

class Net(IO):
    pass

class IP(Net):
    def __init__(self, V):
        IP.validate(V)
        super().__init__(V)

    lex = r'(\d{1,3}\.){3}\d{1,3}'

    @staticmethod
    def validate(V):
        assert re.match(IP.lex, V)
        for i in map(int, V.split('.')):
            assert i <= 255

class Port(Net, Int):
    @staticmethod
    def validate(V):
        assert isinstance(V, int)
        assert V >= 0 and V < 0x10000

    def __init__(self, V):
        Port.validate(V)
        Int.__init__(self, V)

class EMail(Net):
    def html(self, depth=0):
        return f'<a href="mailto:{self.value}">{self.value}</a>'

class Url(Net):
    def html(self, depth=0):
        return f'<a href="{self.value}">{self.value}</a>'
