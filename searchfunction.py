import os.path
import sys
import sqlite3
#import pandas as pd 
import os.path
import datetime
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response, send_file
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


class SearchForm(FlaskForm):
    search_query = StringField('')
    submit = SubmitField('Search')

conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()

def search2(query):
    # Execute the SELECT statement
    cursor.execute("SELECT * FROM vragen WHERE vraag LIKE ?", (f"%{query}%",))
    # Fetch the results
    results = cursor.fetchone()
    return results


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search_query.data
        results = search2(query)
        print(results)
        return render_template('results.html', results=results)
    return render_template('search.html', form=form)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)