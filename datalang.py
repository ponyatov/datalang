import config

import os, sys, re
import traceback

################################################################## object core

class Object:
    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.slot = {}
        self.nest = []

    ##################################################### dump

    def test(self): return self.dump(test=True)

    def __repr__(self): return self.dump()

    def dump(self, cycle=[], depth=0, prefix='', test=False):
        ret = self.pad(depth) + self.head(prefix, test)
        # block cycles
        if not depth: cycle=[]
        if self in cycle: return ret + ' _/'
        else: cycle.append(self)
        # slot{}
        for i in sorted(self.slot.keys()):
            ret += self.slot[i].dump(cycle, depth + 1, f'{i} = ', test)
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j} : ', test)
        return ret

    def head(self, prefix='', test=False):
        suffix = '' if test else f' @{id(self):x}'
        return f'{prefix}<{self.type}:{self.value}>{suffix}'

    def pad(self, depth):
        return '\n' + '\t' * depth

    ############################################### operators

    def keys(self):
        return sorted(self.slot.keys())

    def __getitem__(self, key):             ## A[key] get by symbol
        assert isinstance(key, str)
        return self.slot[key]

    def __setitem__(self,key,that):         ## A[key] = B
        assert isinstance(key,str)
        if isinstance(that,str):
            that = Str(that)
        if isinstance(that,int):
            that = Int(that)
        assert isinstance(that,Object)
        self.slot[key] = that ; return self

    def __lshift__(self,that):              ## A[B.type] = B
        assert isinstance(that,Object)
        return self.__setitem__(that.type,that)

    def __rshift__(self,that):              ## A[B.value] = B
        assert isinstance(that,Object)
        return self.__setitem__(that.value,that)

    def __floordiv__(self, that):           ## A // B push
        assert isinstance(that, Object)
        self.nest.append(that)
        return self

    ############################################## conversion

    def html(self,depth=0):
        raise NotImplementedError(self, 'html', self.__class__)

    ############################################## evaluation

    def eval(self, env):
        raise NotImplementedError(self, 'eval', self.__class__)


###################################################### primitive scalar types

class Primitive(Object):
    def eval(self, env): return self # most pritimives evaluates into itself

class Sym(Primitive):
    def eval(self, env): return env[self.value]

class Str(Primitive):
    def html(self,depth=0): return f'{self.value}'

class Num(Primitive):
    def __init__(self, V):
        super().__init__(float(V))

class Int(Num):
    def __init__(self,V):
        Primitive.__init__(self,int(V))

############################################################# data containers

class Container(Object):
    def __init__(self, V=''):
        super().__init__(V)

    def eval(self, env): return self

class Map(Container):
    pass
class Env(Map):
    pass


env = Env('global') ; env['env'] = env

class List(Container):
    pass

class Stack(Container):
    pass

class Queue(Container):
    pass


################################################# active (executable) objects

class Active(Object):
    pass

class Op(Active):       # operator
    def eval(self, env):
        if len(self.nest) == 1:
            if self.value == '`':
                return self.nest[0]
            raise NotImplementedError(self, 1)
        elif len(self.nest) == 2:
            raise NotImplementedError(self, 2)
        else:
            raise NotImplementedError(self, len(self.nest))

class Cmd(Active):      # VM command (Python function)
    pass

class Fn(Active):       # function
    pass

######################################################################## meta

class Meta(Object): pass

class S(Meta):                              ## generic source code
    def __init__(self,start=None,end=None):
        super().__init__('')
        self.start = start
        self.end = end
    def html(self,depth=0):
        ret = ''
        if self.start:
            ret += f'{" "*depth}{self.start}\n'
        for j in self.nest:
            ret += j.html(depth+1)+'\n'
        if self.end:
            ret += f'{" "*depth}{self.end}\n'
        return ret

######################################################################### I/O

class IO(Object): pass

class Dir(IO): pass
class File(IO): pass

class Net(IO): pass

class IP(Net):
    def __init__(self,V):
        IP.validate(V)
        super().__init__(V)

    lex = r'(\d{1,3}\.){3}\d{1,3}'

    @staticmethod
    def validate(V):
        assert re.match(IP.lex,V)
        for i in map(int,V.split('.')): assert i <= 255

class Port(Net,Int):
    @staticmethod
    def validate(V):
        assert isinstance(V,int)
        assert V >= 0 and V < 0x10000
    def __init__(self,V):
        Port.validate(V)
        Int.__init__(self,V)

class EMail(Net):
    def html(self,depth=0):
        return f'<a href="mailto:{self.value}">{self.value}</a>'

class Url(Net):
    def html(self,depth=0):
        return f'<a href="{self.value}">{self.value}</a>'


####################################################################### lexer


import ply.lex as lex

tokens = ['sym', 'num', 'str',
          'lq', 'rq',
          'comma', 'tild', 'tick',
          ]

t_ignore = ' \t\r'

def t_exit(t):
    r'exit\(\)'
    os._exit(0)

def t_nl(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_str(t):
    r"'.*'|\".*\""
    t.value = Str(t.value[1:-1])
    return t


t_lq = r'\['
t_rq = r'\]'

t_comma = r','
t_tild = r'~'
t_tick = r'`'

def t_num(t):
    r'[+\-]?[0-9]+(\.[0-9]+)?([eE][+\-]?[0-9]+)?'
    t.value = Num(t.value)
    return t

def t_sym(t):
    r'[^ \t\r\n\(\)\[\]\{\}\,\~\`]+'
    t.value = Sym(t.value)
    return t

def t_ANY_error(t): raise SyntaxError(t)


lexer = lex.lex()


####################################################################### parser

import queue

parser_done = queue.Queue()

import ply.yacc as yacc

def p_REPL_none(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    ast = p[2]                                  # parsed AST
    # print('ast:', ast.dump(1))
    try:
        result = p[2].eval(env)                 # evaluated AST
        # print('eval:', result.dump(1))
    except Exception as err:
        result = None
        traceback.print_exc()
    # print('env:', env.dump(1))                # current env state
    # print('-' * 88)                           # ------------------
    parser_done.put([ast, result])


############################################ literals

def p_ex_sym(p):
    ' ex : sym '
    p[0] = p[1]
def p_ex_num(p):
    ' ex : num '
    p[0] = p[1]
def p_ex_str(p):
    ' ex : str '
    p[0] = p[1]

############################################ operators

def p_ex_quote(p):
    ' ex : tick ex '
    p[0] = Op(p[1]) // p[2]

def p_ex_nameit(p):
    ' ex : sym tild ex '
    p[0] = p[3]
    p[3].value = p[1].value

############################################### parens

def p_ex_list(p):
    ' ex : lq seq rq '
    p[0] = p[2]

def p_seq_none(p):
    ' seq : '
    p[0] = List()
def p_list_spaced(p):
    ' seq : seq ex '
    p[0] = p[1] // p[2]
def p_list_comma(p):
    ' seq : seq comma ex '
    p[0] = p[1] // p[3]


def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)

##################################################################### metainfo

metainfo = Map('metainfo') ; env >> metainfo

class Author(Meta): pass
class GitHub(Meta): pass

metainfo << (Author('Dmitry Ponyatov') << EMail('dponyatov@gmail.com'))
metainfo << GitHub('https://github.com/ponyatov/datalang')

######################################################################## bully

class Module(Meta): pass

class HTML(Object):
    def __init__(self,V=None,**kw):
        super().__init__(V)
        for i in kw:
            j = i.replace('_','-')
            j = j.replace('clazz','class')
            self[j] = kw[i]
    def html(self,depth=0):
        ret = f'{" "*depth}<{self.type}'
        for i in self.keys():
            ret += f' {i}="{self[i].html()}"'
        ret += '>'
        if self.value != None:
            ret += f'{self.value}'
        for j in self.nest:
            ret += j.html(depth+1)
        if self.nest:
            ret += f'{" "*depth}'
        ret += f'</{self.type}>'
        return ret

class HEAD(HTML): pass
class TITLE(HTML): pass
class META(HTML): pass
class LINK(HTML): pass
class SCRIPT(HTML): pass

class BODY(HTML): pass
class DIV(HTML): pass
class NAV(HTML): pass

class A(HTML): pass
class IMG(HTML): pass
class PRE(HTML): pass

class App(Module):
    def __init__(self,V,logo="/static/logo.png"):
        super().__init__(V)
        self['logo'] = File(logo)
        # self['head'] = self.html_head()

    def html_head(self):
        return HEAD() //\
            TITLE(f'{self.head(test=True)[1:-1]}') //\
            META(charset="utf-8") //\
            META(http_equiv="X-UA-Compatible",content="IE=edge") //\
            META(name="viewport",content="width=device-width, initial-scale=1") //\
            LINK(href="/static/bootstrap.css",rel="stylesheet") //\
            (S('<!--[if lt IE 9]>','<![endif]-->') //\
                SCRIPT(src="/static/html5shiv.js") //\
                SCRIPT(src="/static/respond.js")) //\
            LINK(rel="shortcut icon",href=self['logo'].value,type="image/png") //\
            LINK(href="/static/css.css",rel="stylesheet")

    def html(self,depth=0):
        ret = '<!doctype html>'
        #
        head = self.html_head() # self['head']
        #
        body = BODY() //\
            (DIV(clazz="container-fluid") //\
                (NAV(clazz="navbar navbar-default") //\
                    (A(href=f'/dump/app/{self.value}',clazz="navbar-logo") //\
                    IMG(src=self['logo'].value,style="height:48px;",alt=re.sub(r'[<>]','',self.head())))
                )
            )
        #
        script = HTML() //\
            SCRIPT(src="/static/jquery.js") //\
            SCRIPT(src="/static/bootstrap.js")
        #
        ret += (HTML(lang='ru') // head // body // script).html()
        return ret

env >> (Map('app') >> App('bully',logo='/static/weather.png'))


################################################################ web interface

class Web(Object): pass


web = Map('web') ; env >> web
web['host'] = IP(config.HOST)
web['port'] = Port(config.PORT)

import flask

web['engine'] = Module('flask')

app = flask.Flask(__name__)

with app.app_context():
    flask.g.argv = sys.argv

from flaskext.markdown import Markdown
Markdown(app)

##################################################################### database

class DB(Object): pass

db = DB(f'sqlite:///{sys.argv[0]}.db')

env['web'] << db

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db.value
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #
    login = db.Column(db.String(0x11), unique=True, nullable=False)
    #
    email = db.Column(db.String(0x22), nullable=False)
    phone = db.Column(db.String(0x22))
    skype = db.Column(db.String(0x22))
    telegram = db.Column(db.String(0x22))
    #
    first_name = db.Column(db.String(0x11), nullable=False)
    second_name = db.Column(db.String(0x11))
    last_name = db.Column(db.String(0x11), nullable=False)
    #
    admin = db.Column(db.Boolean())

def db_install():
    db.create_all()
    db.session.add(User(login='dponyatov',
                        email='dponyatov@gmail.com', telegram='dponyatov',
                        first_name='Dmitry', last_name='Ponyatov',
                        admin=True))
    db.session.commit()


###################################################################### routing

@app.route('/', methods=['GET', 'POST'])
def index():
    # assert request.method == 'GET'
    return flask.render_template('index.html', argv=sys.argv)

@app.route('/admin/')
def admin():
    # return flask.redirect('/')
    return flask.render_template('admin.html', argv=sys.argv, User=User)

@app.route('/about/')
def about():
    with open('README.md') as md:
        README = md.read()
    return flask.render_template('about.html', argv=sys.argv, readme=README)

@app.route('/static/<path:path>')
def statics(path):
    print(path)
    return app.send_static_file(path)

@app.route('/dump/<path:path>')
def dump(path):
    item = env
    for i in re.findall(r'[a-z]+',path):
        item = item[i]
    return flask.render_template('dump.html',data=item.dump())

@app.route('/<path:path>')
def any(path):
    item = env
    for i in re.findall(r'[a-z]+',path):
        item = item[i]
    return item.html()


########################################################## system command line

def bar(): print('-' * 88)

def REPL():
    print(env['metainfo'])
    bar()
    while True:
        while parser_done.empty():
            try: parser.parse(input('data> '))
            except SyntaxError: traceback.print_exc()
        ast,result = parser_done.get(timeout=1)
        #
        print('ast:', ast.dump(1))          # parsed AST
        if result:
            print('eval:', result.dump(1))  # evaluated AST
        print('env:', env.dump(1))          # current env state
        bar()                               # ------------------

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        print('run `make web`     for web interface run')
        print('run `make install` for database init')
        print('run `make repl`    for interactive console shell')
    elif sys.argv[1] == 'web':
        app.run(host=config.HOST, port=config.PORT, debug=True)
    elif sys.argv[1] == 'install':
        db_install()
    elif sys.argv[1] == 'repl':
        REPL()
    else:
        raise SyntaxError(sys.argv)
