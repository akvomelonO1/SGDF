from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify
)
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import time

app = Flask(__name__)

app.secret_key = 'impossible key'

#DB CONNECTION
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SGDF'

#INIT MYSQL
mysql = MySQL(app)
@app.route('/')
def indexRedirect():
    return redirect(url_for('login'))

def loginCheck(username,password):
    #CHECK IF USER EXISTS IN DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE dbusername = %s AND dbpassword = %s', (username,password,))
        user = cursor.fetchone()
        
        #CREATE A SESSION DATA TO ACCES FROM OTHER ROUTES
        #THIS DATA WILL WORK AS WELL AS COOKIES
        if user:
            print(username,password)
            session['loggedin'] = True
            session['id'] = user['id']
            session['dbusername'] = user['dbusername']
            #REDIRECT TO HOME PAGE
            msg = '* Logged in SUCCESSFULLY 🥳 *'
            time.sleep(3)
            return render_template('login.html',msg = msg)
            return True
        else:
            msg = '* INCORRECT username/ password (TRY AGAIN) 🥴 * '
            time.sleep(3)
            return render_template('login.html',msg = msg)
            return False



#SET UP THE LOGIN PAGE WITH POST AND GET METHODS
@app.route('/login/',methods=['GET','POST'])
def login():
    #TO CONTROL ERROR MESSAGE 
    msg = ''
    #CHECK IF USER AND PASSWORD INPUTS ARE EMPTY OR NOT
    if request.method == 'POST' and 'fusername' in request.form and 'fpassword' in request.form:
        username = request.form['fusername']
        password = request.form['fpassword']
        loginCheck(username,password)
        if loginCheck:
            
            return redirect(url_for('uploadFiles'))
        else:
            
            return redirect(url_for('login'))
    return render_template('login.html')

#SET UP FUNCTION TO UPLOAD FILES 
@app.route('/login/uploadFiles', methods=['GET','POST'])
def uploadFiles():
    #TO CONTROL ERROR MESSAGE 
    return render_template('uploadFiles.html')

#SETUP LOGOUT PAGE
@app.route('/login/logout')
def logout():
    #REMOVE SESSION DATA TO LOGOUT
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('dbusername', None)
    
    #REDIRECT TO LOGIN PAGE
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)