from .string import *
from .web import *

class HTML(Web):
    def __init__(self, V=None, **kw):
        super().__init__(V)
        for i in kw:
            j = i.replace('_', '-')
            j = j.replace('clazz', 'class')
            assert isinstance(kw[i], str)
            self[j] = Str(kw[i])

    def html(self, depth=0):
        ret = f'{" "*depth}<{self.type}'
        for i in self.keys():
            ret += f' {i}="{self[i].html()}"'
        ret += '>'
        if self.value != None:
            ret += f'{self.value}'
        for j in self.nest:
            ret += j.html(depth + 1)
        if self.nest:
            ret += f'{" "*depth}'
        ret += f'</{self.type}>'
        return ret


class HEAD(HTML):
    pass
class TITLE(HTML):
    pass
class META(HTML):
    pass
class LINK(HTML):
    pass
class SCRIPT(HTML):
    pass


class BODY(HTML):
    pass
class DIV(HTML):
    pass
class SPAN(HTML):
    pass
class NAV(HTML):
    pass


class P(HTML):
    pass
class A(HTML):
    pass
class IMG(HTML):
    pass
class PRE(HTML):
    pass


class TABLE(HTML):
    pass
class TR(HTML):
    pass
class TD(HTML):
    pass
