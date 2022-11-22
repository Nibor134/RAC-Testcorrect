import os.path
import sys

from flask import Flask, render_template, redirect, url_for, request, session, g

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.
class User:
    def __init__(self, id , username, password):
        self.id = id
        self.username = username
        self.password = password

    def _repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Robin', password='Winkels'))
users.append(User(id=2, username='Max', password='Looij'))
users.append(User(id=3, username='Stan', password='Verdoorn'))
users.append(User(id=4, username='Alex', password='Elwuar'))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user = [x for x in users if x.username == username][0]

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('menu'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('login'))
        
    return render_template('login2.html', error=error)

@app.route("/menu")
def menu():
    if not g.user:
        return redirect(url_for('login'))

    return render_template ("Menu2.html")

@app.route("/tables")
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )

@app.route("/editor")
def editor():
    tables = dbm.get_table_list()
    return render_template(
        "editor.html", table_list=tables, database_file=DATABASE_FILE
    )

# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
