import config

import os, sys
import traceback

import flask

app = flask.Flask(__name__)

with app.app_context():
    flask.g.argv = sys.argv

from flaskext.markdown import Markdown
Markdown(app)


##################################################################### database

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sys.argv[0]}.db'
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
    assert request.method == 'GET'
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

    def dump(self, depth=0, prefix='', test=False):
        ret = self.pad(depth) + self.head(prefix, test)
        # slot{}
        for i in sorted(self.slot.keys()):
            ret += self.slot[i].dump(depth + 1, f'{i} = ', test)
        for j, k in enumerate(self.nest):
            ret += k.dump(depth + 1, f'{j} : ', test)
        return ret

    def head(self, prefix='', test=False):
        suffix = '' if test else f' @{id(self):x}'
        return f'{prefix}<{self.type}:{self.value}>{suffix}'

    def pad(self, depth):
        return '\n' + '\t' * depth

    ############################################### operators

    def __getitem__(self, key):             ## A[key] get by symbol
        assert isinstance(key, str)
        return self.slot[key]

    def __floordiv__(self, that):           ## A // B push
        assert isinstance(that, Object)
        self.nest.append(that)
        return self

    ############################################## evaluation

    def eval(self, env): raise NotImplementedError(self, eval, self.__class__)


###################################################### primitive scalar types

class Primitive(Object):
    def eval(self, env): return self # most pritimives evaluates into itself

class Sym(Primitive):
    def eval(self, env): return env[self.value]

class Str(Primitive):
    pass

class Num(Primitive):
    def __init__(self, V):
        super().__init__(float(V))


############################################################# data containers

class Container(Object):
    def __init__(self, V=''):
        super().__init__(V)

    def eval(self, env): return self

class Map(Container):
    pass
class Env(Map):
    pass


env = Env('global')

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


########################################################## system command line

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
        while True:
            parser.parse(input('data> '))
    else:
        raise SyntaxError(sys.argv)
