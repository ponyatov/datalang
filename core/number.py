from .primitive import *

## floating point number (more generic)
class Num(Primitive):
    def __init__(self, V):
        super().__init__(float(V))

## integer number (special cases like counting)
class Int(Num):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
