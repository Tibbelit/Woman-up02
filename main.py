from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH, get, post
from datetime import datetime, date
import sqlite3
import bottle
from bottle.ext import beaker
import os

abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path)

session_opts = {
    'session.type': 'database',
    'session.data_dir': 'woman-up.db',
    'session.cookie._expires': True,
    'sessison.timeout': 1440,
    'session.auto': True,
}

inloggad = "None"


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)


@route("/startpage")
def startpage():
    return template("startpage")


@route("/", method=["POST", "GET"]) 
def login():
    global inloggad
    ''' Loginsidan'''
    msg = ""
    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')
    conn = sqlite3.connect('woman-up.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE email = ? and password = ?',(email, password))
    user = c.fetchone()
    if user:
        c.execute('SELECT email FROM user WHERE email = ?', (email))
        uid = c.fetchone
        sess = request.environ.get('beaker.session')
        sess['uid'] = uid
        redirect('/startpage') 
    else:
        msg = "Inkorrekt email eller lösenord"

    return template('index', msg=msg)


@route('/register', method=["POST", "GET"])
def register():
    msg = ""
    if request.method =="POST":
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
            c.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?,?)',(firstname, lastname, phonenumber, password, email, None, None, None))
            conn.commit()
            redirect('/')

    return template('register', msg=msg)


@route("/FullPrivacyPolicy")
def popup():
    return template("FullPrivacyPolicy")


@route('/map', method=["POST", "GET"])
def map(): 
    global inloggad
    print(inloggad)
    conn = sqlite3.connect("woman-up.db")
    cursor= conn.cursor()
    inloggad = "" ##den som är inloggad
    klart = ""
    if request.method == 'POST':
        print("Post")
         ### den som är inloggad
        all_location = getattr(request.forms, 'spara_plats') ## ser ut long,lat,offset
        list_location = all_location.split(",") ##delar upp i array
        print(list_location)
        sql = "UPDATE user SET long ="+list_location[0]  +", lat =" + list_location[1]+ ", offset = "+list_location[2]+ " WHERE email = '"+ inloggad +"'"
        print("ok")
        klart = "Din plats är uppdaterad"
        cursor.execute(sql)
        
    location=[] #alla som ska skrivas ut på kartan sparas här
    sql = "select first_name,long,lat,offset from user where email != '" + inloggad+"'"
    print(sql)
    cursor.execute(sql)
    for x in cursor:
        location.append(x)
    print(location)
    conn.commit()

    return template('map',location=location, klart=klart)

@route('/emergency')
def emergency():
    return template('emergency')


@route('/chatt')
def chatt():
    return template('chatt')


run(host='localhost', port=8083, debug=True, reloader=True)
