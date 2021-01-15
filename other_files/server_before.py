from flask import Flask, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2 

app = Flask(__name__)

def connect():
    try:
        conn = psycopg2.connect(
            database = "mentordb",
            user = "postgres",
            host = "localhost",
            port = "5432",
            password = "postgres"
        )

        cur = conn.cursor()

    except(Exception, psycopg2.DatabaseError) as error:      
        print("Error while creating PostgreSQL table", error) 

def create_table():
    conn = connect()
    cur = connect()
    
    try:
        query = """
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                f_name VARCHAR(30) NOT NULL,
                s_name VARCHAR(30),
                surname VARCHAR(30) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password TEXT NOT NULL )
        """
        cur.execute(query)
        cur.commit()

    except:
        print('ERROR!')
    
    conn.close()
    
def insert_user(f_name, s_name, surname, email, password): 
    conn, cur = connect() 
  
    try: 
        hashed_val = generate_password_hash(password)
        # inserting values into the users table 
        cur.execute('INSERT INTO users (DEFAULT, f_name, s_name, surname, email, password) VALUES(%s, %s, %s, %s)', 
                                    (f_name, s_name, surname, email, hashed_val)) 

    except Exception as err: 
  
        print('ERROR!', err) 
    # commiting the transaction. 
    conn.commit() 
    conn.close()

def fetch_user(id):
    conn, cur = connect() 

    # select all the rows from emp 
    try:
        sql = "SELECT * FROM users WHERE user_id = %s"
        user_id = id
        cur.execute(sql, user_id) 
    except: 
        print('ERROR!') 
  
    # store the result in data 
    data = cur.fetchall() 
  
    conn.close()
    # return the result 
    return data 

# a function to print the users 
def print_data(data): 
  
    print('Query result: ') 
    print() 
  
    # iterating over all the  
    # rows in the table 
    for row in data: 
  
        # printing the columns 
        print('id: ', row[0]) 
        print('First Name: ', row[1]) 
        print('Second Name: ', row[2]) 
        print('Email: ', row[3]) 
        print('----------------------------------') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

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
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    create_table()
    app.run(debug=True)