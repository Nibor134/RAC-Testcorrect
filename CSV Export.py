import sqlite3
import pandas as pd 
#import sqlalchemy

#SQL steps
#select * from auteurs
#select * from leerdoelen
#select * from vragen

connection = sqlite3.connect('testcorrect_vragen.db')
cursor = connection.cursor()
sqlquery = 'SELECT * FROM Auteurs'
cursor.execute(sqlquery)
result = cursor.fetchall()
for row in result: 
    df = pd.read_sql_query(sqlquery,connection)
    df.to_csv('output.CSV', index = False)