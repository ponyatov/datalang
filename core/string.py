from .primitive import *

## string
class Str(Primitive):
    def html(self, depth=0): return f'{self.value}'
