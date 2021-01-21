
class Object:

    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.slot = {}
        self.nest = []

    ##################################################### dump

    ## pytest callback: remove hashes, id(self),..
    def test(self): return self.dump(test=True)

    ## print callback
    def __repr__(self): return self.dump()

    ## short <T:V> header-only dump
    def head(self, prefix='', test=False):
        suffix = '' if test else f' @{id(self):x}'
        return f'{prefix}<{self.type}:{self.value}>{suffix}'

    ## full tree text dump
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        ret = self.pad(depth) + self.head(prefix, test)
        # block cycles
        if not depth:
            cycle = []
        if self in cycle:
            return ret + ' _/'
        else:
            cycle.append(self)
        # slot{}
        for i in sorted(self.slot.keys()):
            ret += self.slot[i].dump(cycle, depth + 1, f'{i} = ', test)
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j} : ', test)
        return ret

    ## tree padding
    def pad(self, depth):
        return '\n' + '\t' * depth

    ############################################### operators

    ## A.keys() sorted
    def keys(self):
        return sorted(self.slot.keys())

    ## A[key] get by symbol
    def __getitem__(self, key):
        assert isinstance(key, str)
        return self.slot[key]

    ## A[key] = B
    def __setitem__(self, key, that):
        assert isinstance(key, str)
        assert isinstance(that, Object)
        self.slot[key] = that
        return self

    ## A[B.type] = B
    def __lshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.type, that)

    ## A[B.value] = B
    def __rshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.value, that)

    ## A // B push
    def __floordiv__(self, that):
        assert isinstance(that, Object)
        self.nest.append(that)
        return self

    ############################################## evaluation

    ## evaluate subgraph in [env]ironment
    def eval(self, env):
        raise NotImplementedError(self, 'eval', self.__class__)
