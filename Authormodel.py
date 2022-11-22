import os.path

from flask import Flask, render_template, redirect, url_for, request
from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database


app = Flask(__name__)

DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
db = DatabaseModel(DATABASE_FILE)


class AuthorModel(db.Model):
    __tablename__ = "table"
 
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))
 
    def __init__(self, author_id,name,age,position):
        self.author_id = author_id
        self.name = name
        self.age = age
        self.position = position
 
    def __repr__(self):
        return f"{self.name}:{self.author_id}

@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    Author = AuthorModel.query.filter_by(Author_id=id).first()
    if request.method == 'POST':
        if Author:
            db.session.delete(Author)
            db.session.commit() 
            firstname = request.form['voornaam']
            lastname = request.form['Achternaam']
            year_of_birth = request.form['Geboortejaar']
            employee = request.form['Medewerker']
            retired = request.form['met pensioen']
            Author = AuthorModel(Author_id=id, firstname=firstname, year_of_birth=year_of_birth, lastname=lastname, employee=employee, retired=retired)
 
            db.session.add(Author)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Autheur met id = {id} bestaat niet"
 
    return render_template('update.html', Author = Author)