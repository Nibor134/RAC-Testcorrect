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

@app.route("/editor/auteurs", methods=('GET', 'POST'))
def auteureditor():
    con = sqlite3.connect(db_local)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from auteurs")
    #cur.execute("SELECT * FROM vragen WHERE auteur NOT IN (SELECT id FROM auteurs)")  
    rows = cur.fetchall()  
    return render_template("Auteureditor.html",rows = rows)

@app.route("/editor/auteurs/update/<int:id>", methods = ['GET','POST'])
def update(id):
    con = sqlite3.connect(db_local)
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











if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
