from .container import *
from .meta import *
from .net import *

class Author(Meta):
    pass

class GitHub(Url):
    pass


metainfo = Map('metainfo')

metainfo << (Author('Dmitry Ponyatov')
             << EMail('dponyatov@gmail.com'))
metainfo << GitHub('https://github.com/ponyatov/datalang')
