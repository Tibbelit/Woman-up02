from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH, get, post
from datetime import datetime, date
import sqlite3
import os
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)


@route('/startpage')
def startpage():
    return template('startpage')


@get('/')
def login_page():
       return template('index', msg="")


@post('/')
def login():
    ''' Loginsidan'''
    msg = ""
   
    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')
    conn = sqlite3.connect('woman-up.db')
    c = conn.cursor()
    #find_user = ("SELECT * FROM user WHERE email = ? and password = ?")
    c.execute('SELECT * FROM user WHERE email = ? and password = ?',(email, password))
    if c.fetchone():
        redirect('/startpage') 
    else:
        msg = "Inkorrekt email eller lösenord"

    return template('index', msg=msg)

@get('/register')
def register_page():
        return template('register', msg="")


@post('/register')
def register():
    msg = ""
    firstname = getattr(request.forms, 'firstname')
    lastname = getattr(request.forms, 'lastname')
    phonenumber = getattr(request.forms, 'phonenumber')
    password = getattr(request.forms, 'password')
    email = getattr(request.forms, 'email')
    conn = sqlite3.connect('woman-up.db')
    c = conn.cursor()
  
    c.execute('SELECT * FROM user WHERE email = ?', (email,))
    if c.fetchone():
         msg = "Den email adressen är reddan registrerad"
    elif not password or not email:
         msg = "Vänligen uppge all uppgifter"
    else:
        c.execute('INSERT INTO user VALUES(?,?,?,?,?)',(firstname, lastname, phonenumber, password, email))
        conn.commit()
        redirect('/update')


    return template('register', msg=msg)
    

@route('/update')
def new_user():
    return template('update')

run(host='localhost', port=8080, debug=True, reloader=True)
