import sqlite3

conn = sqlite3.connect('db_files.sqlite')
cursor = conn.cursor()
conn.close()

# https://habrahabr.ru/post/321510/