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

d.execute(""" INSERT INTO Users (username, password) VALUES
('Robin', 'Winkels'),
('Max', 'Looij'),
('Stan', 'Verdoorn'),
('Alex', 'Elwuar')
""")

dbm.commit()
dbm.close()