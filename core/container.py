from .object import *


## data container
class Container(Object):

    ## default unnamed
    def __init__(self, V=''):
        super().__init__(V)

    ## evaluates to itself
    def eval(self, env): return self


## ordered list/vector
class List(Container):
    pass


## associative array map/dict
class Map(Container):
    pass


## LIFO
class Stack(Container):
    pass


## FIFO
class Queue(Container):
    pass
