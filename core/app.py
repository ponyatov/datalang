from .io import *
from .meta import *
from .html import *
from .source import *

import re

class App(Module):
    def __init__(self, V, logo="/static/logo.png"):
        super().__init__(V)
        self['logo'] = File(logo)
        # self['head'] = self.html_head()
        self['body'] = HTML()
        self['script'] = S()

    def html_head(self):
        return HEAD() //\
            TITLE(f'{self.head(test=True)[1:-1]}') //\
            META(charset="utf-8") //\
            META(http_equiv="X-UA-Compatible", content="IE=edge") //\
            META(name="viewport", content="width=device-width, initial-scale=1") //\
            LINK(href="/static/bootstrap.css", rel="stylesheet") //\
            (S('<!--[if lt IE 9]>', '<![endif]-->') //
                SCRIPT(src="/static/html5shiv.js") //
                SCRIPT(src="/static/respond.js")) //\
            LINK(rel="shortcut icon", href=self['logo'].value, type="image/png") //\
            LINK(href="/static/css.css", rel="stylesheet")

    def html(self, depth=0):
        ret = '<!doctype html>'
        #
        head = self.html_head() # self['head']
        #
        container = DIV(clazz="container-fluid")
        body = BODY() //\
            (container //
                (NAV(clazz="navbar navbar-default") //
                    (A(href=f'/dump/app/{self.value}', clazz="navbar-logo") //
                     IMG(src=self['logo'].value, style="height:48px;", alt=re.sub(r'[<>]', '', self.head())))
                 )
             )
        try:
            container // self['body']
        except KeyError:
            pass
        #
        try:
            js = self['script']
        except KeyError:
            js = ''
        #
        script = HTML() //\
            SCRIPT(src="/static/jquery.js") //\
            SCRIPT(src="/static/bootstrap.js") //\
            js
        #
        ret += (HTML(lang='ru') // head // body // script).html()
        return ret
