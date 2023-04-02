# Run this to program to wipe the pre-exisiting database (if it exists)
# and create a new, empty one

import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
