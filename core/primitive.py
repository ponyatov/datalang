from .object import *

## primitive scalar type
class Primitive(Object):
    ## most pritimives evaluates into itself
    def eval(self, env): return self

## symbol/name/atom
class Sym(Primitive):
    ## evaluates via environment lookup
    def eval(self, env): return env[self.value]
