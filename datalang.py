import config

import os, sys

import flask

app = flask.Flask(__name__)

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
                        email='dponyatov@gmail.com',telegram='dponyatov',
                        first_name='Dmitry',last_name='Ponyatov',
                        admin=True))
    db.session.commit()


###################################################################### routing

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/admin/')
def admin():
    # return flask.redirect('/')
    return flask.render_template('admin.html',User=User)

@app.route('/about/')
def about():
    with open('README.md') as md: README = md.read()
    return flask.render_template('about.html',readme=README)

@app.route('/static/<path:path>')
def statics(path):
    print(path)
    return app.send_static_file(path)


########################################################## system command line

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        app.run(host=config.HOST, port=config.PORT, debug=True)
    elif sys.argv[1] == 'install':
        db_install()
    else:
        raise SyntaxError(argv)
