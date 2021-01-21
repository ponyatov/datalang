from .container import *

## environment
class Env(Map):
    pass


## global namespace
env = Env('global')

## cyclic reference (mostly for Web API)
env['env'] = env
