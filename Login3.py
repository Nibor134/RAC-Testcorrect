import os.path
import sys
import sqlite3

from flask import Flask, render_template, redirect, url_for, request, session, g, flash, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


#Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

DATABASE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')
dbm = DatabaseModel(DATABASE)

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, password):
         self.id = id
         self.username =  username
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id

class LoginForm(FlaskForm):
 username = StringField('Username',validators=[DataRequired()])
 password = PasswordField('Password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')
 def validate_username(self, username):
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("SELECT username FROM Users where username = (?)",[username.data])
    valemail = curs.fetchone()
    if valemail is None:
      raise ValidationError('This Username ID is not registered. Please register before login')

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect(DATABASE)
   curs = conn.cursor()
   curs.execute("SELECT * from Users where id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('menu'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = sqlite3.connect(DATABASE)
     curs = conn.cursor()
     curs.execute("SELECT * FROM Users where username = (?)",    [form.username.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     if form.username.data == Us.username and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        list({form.username.data})[0]
        flash('Logged in successfully ')
        redirect(url_for('menu'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login3.html', title='Login', form=form)

@app.route("/menu", methods=('GET', 'POST'))
def menu():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT COUNT (*) FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)")
    count = cur.fetchone()[0]
    print(count)
    con.commit()
    cur.execute("SELECT COUNT (*) FROM vragen WHERE vraag LIKE '%<br>%'")
    count2 = cur.fetchone()[0]
    print(count2)
    con.commit()
    cur.execute("SELECT COUNT (*) FROM vragen WHERE vraag LIKE '%&nbsp;%'")
    count3 = cur.fetchone()[0]
    print(count3)
    con.commit()
    cur.execute("SELECT COUNT (*) FROM vragen WHERE auteur NOT IN (SELECT id FROM auteurs)")
    count4 = cur.fetchone()[0]
    print(count4)
    con.commit()
    return render_template ("dashboard.html", count=count, count2=count2, count3=count3,count4=count4)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
