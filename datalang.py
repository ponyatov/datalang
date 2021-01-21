import config

import os, sys, re
import traceback

################################################################## object core

from core.object import *

class Object(Object):

    ############################################## conversion

    def html(self, depth=0):
        raise NotImplementedError(self, 'html', self.__class__)


###################################################### primitive scalar types

from core.primitive import *
from core.string import *
from core.number import *

############################################################# data containers

from core.container import *
from core.namespace import *

################################################# active (executable) objects

from core.active import *

######################################################################## meta


from core.meta import *
from core.source import *

######################################################################### I/O

from core.io import *
from core.net import *

####################################################################### parser

from core.parser import *

##################################################################### metainfo

from core.metainfo import *

env >> metainfo

######################################################################### html

from core.web import *
from core.html import *

################################################################## application

from core.app import *


env >> Map('app')

###################################################################### DataWeb

dataweb = App('dataweb')
env['app'] >> dataweb

dataweb['logo'] = File('/static/datahex.png')

######################################################################## bully

from app.generic import *

bully = App('bully', logo='/static/weather.png')
env['app'] >> bully

def timestamp():
    return \
        (DIV() //
            (P(id="shortdate") // Fn(shortdate)) //
            (P(id="localtime") // Fn(localtime))
         )


env['app'] >> Fn(shortdate) >> Fn(localtime) >> Fn(timestamp)

class Template(HTML):
    def __init__(self, filename):
        assert re.match(r'.+\.(html|js)$', filename)
        super().__init__(filename)

    def html(self, depth=0):
        ret = flask.render_template(self.value, env=env)
        if self.value[-3:] == '.js':
            sid = re.sub(r'[/\.]', r'_', self.value)
            return f'<script id="{sid}">\n{ret}\n</script>'
        else:
            return ret


bully['body'] = (TABLE(id='report') //
                 Template('bully/head.html'))

bully['script'] = (S() // Template('bully/localtime.js'))

################################################################ web interface


web = Map('web')
env >> web
web['host'] = IP(config.HOST)
web['port'] = Port(config.PORT)
web << AJAX(__name__)

import flask

web['engine'] = Module('flask')

app = flask.Flask(__name__)

with app.app_context():
    flask.g.argv = sys.argv

from flaskext.markdown import Markdown
Markdown(app)

##################################################################### database

class DB(Object):
    pass


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
    for i in re.findall(r'[a-z]+', path):
        item = item[i]
    return flask.render_template('dump.html', data=item.dump())

@app.route('/html/<path:path>')
def ajax_html(path):
    item = env
    for i in re.findall(r'[a-z]+', path):
        item = item[i]
    return item.html()

@app.route('/ajax/<path:path>')
def ajax(path):
    item = env
    for i in re.findall(r'[a-z]+', path):
        item = item[i]
    return item.ajax()

@app.route('/<path:path>')
def any(path):
    item = env
    for i in re.findall(r'[a-z]+', path):
        item = item[i]
    return item.html()


########################################################## system command line

def bar(): print('-' * 66)

def REPL():
    print(env['metainfo'])
    bar()
    while True:
        while parser_queue.empty():
            try:
                parser.parse(input('data> '))
            except SyntaxError:
                traceback.print_exc()
        ast, result = parser_queue.get(timeout=1)
        #
        print('ast:', ast.dump(1))          # parsed AST
        if result:
            print('eval:', result.dump(1))  # evaluated AST
        # print('env:', env.dump(1))          # current env state
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
