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

@app.route("/editor/leerdoelen", methods=('GET', 'POST'))
def leerdoelen():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)")
    rows = cur.fetchall()
    return render_template("leerdoelen.html", rows = rows)

@app.route("/editor/leerdoelen/update/<int:id>", methods = ['GET','POST'])
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
 
    cur.execute('SELECT leerdoel FROM vragen WHERE ID = ?', (id,))
    leerdoel = cur.fetchone()[0]
    cur.execute('SELECT  vraag FROM vragen WHERE ID = ?', (id,))
    vraag = cur.fetchone()[0]
    cur.execute('SELECT auteur FROM vragen WHERE ID = ?', (id,))
    auteur = cur.fetchone()[0]
    con.commit()
    con.close
    
    return render_template('leerdoelen.html', leerdoel=leerdoel,vraag=vraag, auteur=auteur)











if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
