import os.path
import sys
import sqlite3

from flask import Flask, render_template, redirect, url_for, request, session, g, flash, abort, render_template_string

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database

#Flask Settings
LISTEN_ALL = "localhost"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 80
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

db_local = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')
db = sqlite3.connect(db_local)
dbm = DatabaseModel(db_local)

d = db.cursor()

#Creating model table for our CRUD database
class Data():
    db = sqlite3.connect(db_local)
    id = db.execute(("SELECT id FROM vragen"))
    leerdoel = db.execute(("SELECT leerdoel FROM vragen"))
    vraag = db.execute(("SELECT vraag FROM vragen"))
    auteur = db.execute(("SELECT auteur FROM vragen"))
 
 
    def __init__(self, leerdoel, vraag, auteur):
 
        self.leerdoel = leerdoel
        self.vraag = vraag
        self.auteur = auteur

@app.route("/editor/htmlcleaner")
def htmleditor():
    con = sqlite3.connect(db_local)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%'")  
    rows = cur.fetchall()  
    return render_template("HTMLupdate.html",rows = rows)

@app.route("/editor/htmlcleaner/update/<int:id>", methods = ['GET','POST'])
def htmlupdate(id):
    con = sqlite3.connect(db_local)
    cur = con.cursor()
    if request.method == 'POST':

        vragen_id =         request.form['id']
        #vragen_leerdoel =   request.form['leerdoel']
        vragen_vraag =      request.form['vraag']
        #vragen_auteur =     request.form['auteur']

        cur.execute("UPDATE vragen SET vraag = ? WHERE id = ?",(vragen_vraag, vragen_id))
        con.commit()
        flash("Vraag succesvol aangepast")  
        return redirect('/htmleditor')
    cur.execute('SELECT * FROM vragen WHERE ID = ?', (id,))
    vragen = cur.fetchone

    con.close

    return render_template('HTMLeditor.html', vragen=vragen)
    

#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    dbm = sqlite3.connect(db_local) 
    all_data = dbm.fetchall()
 
    return render_template("index.html", vragen = all_data)
 
 
 
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        leerdoel = request.form['leerdoel']
        vraag = request.form['vraag']
        auteur = request.form['auteur']
 
 
        my_data = Data(leerdoel, vraag, auteur)
        dbm.session.add(my_data)
        dbm.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 
#this is our update route where we are going to update our employee
@app.route('/update/vraag/', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        db.execute(("SELECT id FROM vragen"))
 
        request.form['leerdoel']
        request.form['vraag']
        request.form['auteur']
 
        db.commit()
        flash("Vraag succesvol aangepast")
 
        return render_template("HTMLeditor.html")
 
 
 
 
#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))
 
 
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)


