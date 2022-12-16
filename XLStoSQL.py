import pandas as pd
import sqlite3
df = pd.read_excel('databases/Table_complete_HTMLescapechar.xlsx')
conn = sqlite3.connect('HTML_escapecharacters.db')

df.to_sql('my_sql_table', conn='HTML_escapecharacters')