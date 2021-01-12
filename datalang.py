import config

import markdown2 as md

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/admin/')
def admin():
    return flask.redirect('/')
    # return flask.render_template('admin.html')

@app.route('/about/')
def about():
    # https://github.com/trentm/python-markdown2/wiki/Extras
    html = md.markdown_path('README.md', extras=[])
    return flask.render_template('about.html',html=html)

app.run(host=config.HOST, port=config.PORT, debug=True)
