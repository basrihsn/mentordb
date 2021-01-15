from flask import Flask, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2 
from create_table import create_tables
from insert import insert_vendor
from config import config
from user import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17'

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        #user = User.query.filter_by(email=email).first()

        

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        #if not user or not check_password_hash(user.password, password):
         #   flash('Please check your login details and try again.')
          #  return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        return redirect(url_for('profile'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        s_name = request.form.get('s_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        insert_user(f_name, s_name, surname, email, password)
        #insert_user(f_name, s_name, surname, email, password)
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

def get_user(user_id):
    query = ("""
        SELECT * from users WHERE user_id = %s
    """) 
    args = (user_id)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(query, args)
        user = cur.fetchall()
        if user is not None:
            for row in user:
                user = User(row[1], row[2], row[3], row[4], row[5])
                return user
        else:
            return None
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()   

def insert_user(f_name, s_name, surname, email, password):
    query = ("""
        INSERT INTO users (f_name, s_name, surname, email, password)
            VALUES (%s, %s, %s, %s, %s)
    """)
    args = (f_name, s_name, surname, email, password)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(query, args)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE if not exists users ( 
            user_id SERIAL PRIMARY KEY,
            f_name VARCHAR(30) NOT NULL,
            s_name VARCHAR(30),
            surname VARCHAR(30) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password TEXT NOT NULL )       
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        #for command in commands:
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)