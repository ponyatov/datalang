from .object import *
from .container import *

class Web(Object):
    pass

class AJAX(Web, Map):
    pass

class Session(Web):
    pass
