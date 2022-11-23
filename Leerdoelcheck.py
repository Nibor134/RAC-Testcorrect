import os.path
import sys
import sqlite3

from flask import Flask, render_template, redirect, url_for, request, session, g, flash, abort

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database

#Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

db_local = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')
dbm = sqlite3.connect(db_local)

d = dbm.cursor()

@app.route("/leerdoelen", methods=('GET', 'POST'))
def leerdoelen():
    dbm = sqlite3.connect(db_local)
    dbm.row_factory = sqlite3.Row
    d = dbm.cursor()
    d.execute("SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)")
    rows = d.fetchall()
    
    return render_template("leerdoelen.html", rows = rows)

@app.route("/leerdoelen", methods=('GET', 'POST'))
def update(d):
    if request.method == 'POST':
        if leerdoelen:
            d.execute.delete(leerdoelen)
            d.execute.commit()
 
            id = request.form['id']
            leerdoelen = request.form['leerdoelen']
            vraag = request.form['vraag']
            auteur = request.form['auteur']
 
            d.execute.add(leerdoelen)
            d.execute.commit()
            return redirect(f'/data/{leerdoelen}')
        return f"Vraag with leerdoel = {leerdoelen} Does not exist"
 
    return render_template('update.html', leerdoelen = leerdoelen)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)