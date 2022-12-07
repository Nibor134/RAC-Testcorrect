import sqlite3
import pandas as pd
import os.path 
#import sqlalchemy

#SQL steps
#select * from auteurs
#select * from leerdoelen
#select * from vragen
DATABASE = os.path.join('databases', 'testcorrect_vragen.db')
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
sqlquery = "SELECT * FROM auteurs"
cursor.execute(sqlquery)
result = cursor.fetchall()
for row in result: 
    df = pd.read_sql_query(sqlquery,connection)
    df.to_csv('output.CSV', index = False)