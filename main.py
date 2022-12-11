import os.path
import sys
import sqlite3
#import pandas as pd 
import os.path
import sqlite3
import datetime
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database
from greeting import get_greeting
from Dayandtime import show_time_in_dutch
from CSV_Export import csv_auteurs,csv_leerdoelen,csv_vragen

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

class LoginForm(FlaskForm):
 username = StringField('Username',validators=[DataRequired()])
 password = PasswordField('Password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')
 def validate_username(self, username):
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("SELECT username FROM Users where username = (?)",[username.data])
    valusername = curs.fetchone()
    if valusername is None:
      raise ValidationError('This username ID is not registered. Please register before login')

class User(UserMixin):
    def __init__(self, id, username, password):
         self.id = id
         self.username = username
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
  greeting = get_greeting()
  if form.validate_on_submit():
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("SELECT * FROM Users where username = (?)",    [form.username.data])
    user = curs.fetchone()
    Us = load_user(user[0])
    if form.username.data == Us.username and form.password.data == Us.password:
        login_user(Us)
        return redirect(('menu'))
    else:
        flash('Login Unsuccessfull.')
    
  return render_template('login.html',title='Login', form=form, greeting = greeting)



@app.route("/menu", methods=('GET', 'POST'))
@login_required
def menu():
    Today = show_time_in_dutch()
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
    cur.execute("SELECT COUNT (*) FROM vragen WHERE leerdoel is NULL;")
    count5 = cur.fetchone()[0]
    con.commit()
    cur.execute("SELECT COUNT (*) FROM vragen WHERE auteur is NULL;")
    count6 = cur.fetchone()[0]
    con.commit()
    return render_template ("dashboard.html",
     count=count, count2=count2, count3=count3,
     count4=count4, count5=count5, count6=count6, Today=Today)

@app.route("/tables")
@login_required
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE
    )
@app.route("/tables/csv_export", methods=('GET', 'POST'))
@login_required
def csv():
    if request.method == 'POST':
        #csv1 = csv_auteurs()
        #csv2 = csv_leerdoelen()
        #csv3 = csv_vragen()
        return redirect(url_for('menu'), csv1=csv1, csv2=csv2, csv3=csv3)

    return render_template(
            "tables_export.html"
    )

@app.route("/editor/auteuren", methods=('GET', 'POST'))
@login_required
def auteuren():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE auteur NOT IN (SELECT id FROM auteurs)")
    rows = cur.fetchall()
    return render_template("Auteuren.html", rows = rows)

@app.route("/editor/auteuren/update/<int:id>", methods = ['GET','POST'])
@login_required
def auteurencheck(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':

        vragen_id =                              id
        vraag      =               request.form['vraag']
        auteur    =               request.form['auteur']
        
        cur.execute("UPDATE vragen SET vraag = ? WHERE id = ?",(vraag, vragen_id))
        cur.execute("UPDATE vragen SET auteur = ? WHERE id = ?",(auteur, vragen_id))
        con.commit()
        flash("Vraag succesvol aangepast")  
        return redirect(url_for('auteuren'))

    
    cur.execute('SELECT vraag FROM vragen WHERE ID = ?', (id,))
    vraag = cur.fetchone()[0]
    cur.execute('SELECT auteur FROM vragen WHERE ID = ?', (id,))
    auteur = cur.fetchone()[0]
    con.commit()
    con.close
    
    return render_template('auteureneditor.html', vraag=vraag, auteur=auteur)




@app.route("/editor/leerdoelen", methods=('GET', 'POST'))
@login_required
def leerdoelen():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)")
    rows = cur.fetchall()
    return render_template("leerdoelen.html", rows = rows)

@app.route("/editor/leerdoelen/update/<int:id>", methods = ['GET','POST'])
@login_required
def leerdoelencheck(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':

        vragen_id =                              id
        leerdoel         =               request.form['leerdoel']
        vraag      =               request.form['vraag']
        auteur    =               request.form['auteur']
        
        cur.execute("UPDATE vragen SET leerdoel = ? WHERE id = ?",(leerdoel, vragen_id))
        cur.execute("UPDATE vragen SET vraag = ? WHERE id = ?",(vraag, vragen_id))
        cur.execute("UPDATE vragen SET auteur = ? WHERE id = ?",(auteur, vragen_id))
        con.commit()
        flash("Vraag succesvol aangepast")  
        return redirect(url_for('leerdoelen'))

    
    
    #Leerdoelen
    cur.execute('SELECT leerdoel FROM leerdoelen WHERE id = 1')
    leerdoel_1 = cur.fetchone()[0]
    cur.execute('SELECT leerdoel FROM leerdoelen WHERE id = 2')
    leerdoel_2 = cur.fetchone()[0]
    
    
    cur.execute('SELECT leerdoel FROM vragen WHERE ID = ?', (id,))
    leerdoel = cur.fetchone()[0]
    cur.execute('SELECT vraag FROM vragen WHERE ID = ?', (id,))
    vraag = cur.fetchone()[0]
    cur.execute('SELECT auteur FROM vragen WHERE ID = ?', (id,))
    auteur = cur.fetchone()[0]
    con.commit()
    con.close
    
    return render_template('leerdoeleneditor.html', leerdoel=leerdoel,vraag=vraag, auteur=auteur,leerdoel_1=leerdoel_1,leerdoel_2=leerdoel_2)



@app.route("/editor/cleaner/")
@login_required
def htmleditor():
    con = sqlite3.connect(DATABASE)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%'")  
    rows = cur.fetchall()  
    return render_template("Testsearchbar.html",rows = rows)


@app.route("/editor/htmlcleaner/update/<int:id>", methods = ['GET','POST'])
@login_required
def update(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':

        vragen_id =             id
        #vragen_leerdoel =   request.form['leerdoel']
        vragen_vraag =          request.form['vraag']
        #vragen_auteur =     request.form['auteur']
        cur.execute("UPDATE vragen SET vraag = ? WHERE id = ?",(vragen_vraag,vragen_id))
        con.commit()
        flash("Vraag succesvol aangepast")  
        return redirect(url_for('htmleditor'))

    cur.execute('SELECT vraag FROM vragen WHERE ID = ?', (id,))
    vragen = cur.fetchone()[0]
    con.commit()
    con.close

    return render_template('HTMLupdate.html', vragen=vragen)

@app.route("/editor/auteurs", methods=('GET', 'POST'))
@login_required
def auteureditor():
    con = sqlite3.connect(DATABASE)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from auteurs")
    #cur.execute("SELECT * FROM vragen WHERE auteur NOT IN (SELECT id FROM auteurs)")  
    rows = cur.fetchall()  
    return render_template("Auteureditor.html",rows = rows)

@app.route("/editor/auteurs/update/<int:id>", methods = ['GET','POST'])
@login_required
def updateauteurs(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':

        auteur_id =                              id
        auteur_voornaam         =               request.form['voornaam']
        auteur_achternaam       =               request.form['achternaam']
        auteur_geboortejaar     =               request.form['geboortejaar']
        auteur_medewerker       =               request.form['medewerker']
        auteur_metpensioen      =               request.form['met pensioen']
        #
        cur.execute("UPDATE auteurs SET voornaam = ? WHERE id = ?",(auteur_voornaam, auteur_id))
        cur.execute("UPDATE auteurs SET achternaam = ? WHERE id = ?",(auteur_achternaam, auteur_id))
        cur.execute("UPDATE auteurs SET geboortejaar = ? WHERE id = ?",(auteur_geboortejaar, auteur_id))
        cur.execute("UPDATE auteurs SET medewerker = ? WHERE id = ?",(auteur_medewerker, auteur_id))
        cur.execute("UPDATE auteurs SET 'met pensioen' = ? WHERE id = ?",(auteur_metpensioen, auteur_id))
        con.commit()
        flash("Vraag succesvol aangepast")  
        return redirect(url_for('auteureditor'))
 
    cur.execute('SELECT voornaam FROM auteurs WHERE ID = ?', (id,))
    voornamen = cur.fetchone()[0]
    cur.execute('SELECT  achternaam FROM auteurs WHERE ID = ?', (id,))
    achternaam = cur.fetchone()[0]
    cur.execute('SELECT geboortejaar FROM auteurs WHERE ID = ?', (id,))
    geboortejaar = cur.fetchone()[0]
    cur.execute('SELECT medewerker FROM auteurs WHERE ID = ?', (id,))
    medewerker = cur.fetchone()[0]
    cur.execute('SELECT "met pensioen" FROM auteurs WHERE ID = ?', (id,))
    metpensioen = cur.fetchone()[0]
    con.commit()
    con.close
    #
    return render_template('Auteurupdate.html', voornamen=voornamen,achternaam=achternaam, geboortejaar=geboortejaar, medewerker=medewerker,metpensioen=metpensioen)
1

@app.route("/editor/NullorNotnullLeer", methods=('GET', 'POST'))
def NullornotNullLeer():
    con = sqlite3.connect(DATABASE)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT * FROM vragen WHERE leerdoel is NULL;")  
    rows = cur.fetchall()  
    return render_template("NullornotNull.html",rows = rows)

@app.route("/editor/NullorNotnullAu", methods=('GET', 'POST'))
@login_required
def NullornotNullAu():
    con = sqlite3.connect(DATABASE)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT * FROM vragen WHERE auteur is NULL;")  
    rows = cur.fetchall()  
    return render_template("NullornotNull.html",rows = rows)




# The table route displays the content of a table
@app.route("/table_details/<table_name>")
@login_required
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.route("/logout")
def logout():
    logout_user()
    return redirect("login")

@app.route("/")
def redirectpage():
    return redirect("login")

    


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)

#CSV export
#connection = sqlite3.connect('testcorrect_vragen.db')
#cursor = connection.cursor()
#sqlquery = 'SELECT * FROM auteurs'
#cursor.execute(sqlquery)
#result = cursor.fetchall()
#for row in result: 
#    df = pd.read_sql_query(sqlquery,connection)
#    df.to_csv('output.CSV', index = False)