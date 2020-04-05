import MySQLdb.cursors
import re
import time
import os
import sqlite3
from flask import (Flask, g, redirect, render_template,
                   request, session, url_for, jsonify)
from flask_mysqldb import MySQL
from flask.helpers import flash
from posix import abort


app = Flask(__name__)

# Cargamos la config desde este mismo archivo
app.config.from_object(__name__)

# Cargamos la config por defecto y sobreeescribimos desde la var de entonro
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'SGDF.db'),
                       SECRET_KEY='impossible key',# podemos crearla con random o algun otro metodo
                       USERNAME='root',
                       PASSWORD='root'))
app.config.from_envvar('SDGF_SETTINGS',silent=True)
# Definimos una var de entorno SDGF_SETTINGS que apunta a un fichero de config que cargará la info. (silent = True, unicamenete le indica a Flask que no pete si no hay un entorno configurado )
# Deberíamos instanciar la BD en otra carpeta, en vez de aquí, pero por el momento ...

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory =sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#NAVEGACIÓN POR EL SISTEMA
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/show_entries')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT * FROM users order by id desc')
    users = cur.fetchall()
    return render_template('show_entries.html',users = users)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into users (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#HASHER LA CONTRASEÑA

