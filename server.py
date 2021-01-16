from flask import Flask, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2 
from create_table import create_tables
from insert import insert_vendor

app = Flask(__name__)

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

        insert_vendor(f_name, s_name, surname, email, password)
        #insert_user(f_name, s_name, surname, email, password)
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)