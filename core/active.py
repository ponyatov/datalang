from .object import *

class Active(Object):
    pass

## VM command (Python function)
class Command(Active):
    pass

## function
class Fn(Active):
    def __init__(self, F):
        assert callable(F)
        super().__init__(F.__name__)
        self.fn = F

    def html(self, depth=0):
        ret = self.fn()
        if isinstance(ret, Object):
            ret = ret.html(depth)
        return ret

    def ajax(self, depth=0):
        return self.fn()


## operator
class Op(Active):
    def eval(self, env):
        if len(self.nest) == 1:
            if self.value == '`':
                return self.nest[0]
            raise NotImplementedError(self, 1)
        elif len(self.nest) == 2:
            raise NotImplementedError(self, 2)
        else:
            raise NotImplementedError(self, len(self.nest))
