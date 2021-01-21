from .meta import *

## generic (nested) source code
class S(Meta):
    def __init__(self, start=None, end=None):
        super().__init__('')
        self.start = start
        self.end = end

    def html(self, depth=0):
        ret = ''
        if self.start:
            ret += f'{" "*depth}{self.start}\n'
        for j in self.nest:
            ret += j.html(depth + 1) + '\n'
        if self.end:
            ret += f'{" "*depth}{self.end}\n'
        return ret
