import sqlite3
import pandas as pd
import os.path 


#SQL steps
#select * from auteurs
#select * from leerdoelen
#select * from vragen

# .,

DATABASE = os.path.join('databases', 'testcorrect_vragen.db')

def csv_auteurs():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sqlquery = "SELECT * FROM auteurs"
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    for row in result: 
        df = pd.read_sql_query(sqlquery,connection)
        df.to_csv('Export/output_auteurs.CSV', index = False)

def csv_leerdoelen():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sqlquery = "SELECT * FROM leerdoelen"
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    for row in result: 
        df = pd.read_sql_query(sqlquery,connection)
        df.to_csv('Export/output_leerdoelen.CSV', index = False)

def csv_vragen():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sqlquery = "SELECT * FROM vragen"
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    for row in result: 
        df = pd.read_sql_query(sqlquery,connection)
        df.to_csv('Export/output_vragen.CSV', index = False)
    