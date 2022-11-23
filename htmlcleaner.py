import os.path
import sys
import sqlite3

from flask import Flask, render_template, redirect, url_for, request, session, g, flash, abort

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
dbm = sqlite3.connect(db_local)

d = dbm.cursor()

@app.route("/editor/htmlcleaner")
def htmleditor():
    con = sqlite3.connect(db_local)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%'")  
    rows = cur.fetchall()  
    return render_template("table_details.html",rows = rows)

@app.route("/editor/htmlcleaner/update", methods = ['GET','POST'])
def htmlupdate():
    con = sqlite3.connect(db_local)  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("UPDATE vragen SET vraag=?")
    rows = cur.fetchall()
    con.commit()
    con.close() 
    return render_template("table_details.html",rows = rows)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)


