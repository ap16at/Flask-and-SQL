# Andrew Perez-Napan
# ap16at
# Due Date: 2-16-21
# The program in this file is the individual work of Andrew Perez-Napan


import sqlite3

conn = sqlite3.connect('reviewData.db')
print("Opened database successfully")

# table is created, FLOATs are kept to 2 decimal places
conn.execute('CREATE TABLE Reviews(Username TEXT(40), Restaurant TEXT(50), ReviewTime DATETIME, Rating FLOAT(2,1), Review TEXT(500))')
print("Table 1 created successfully")

# table is created, FLOATs are kept to 2 decimal places
conn.execute('CREATE TABLE Ratings(Restaurant TEXT, Food FLOAT(2,1), Service FLOAT(2,1), Ambience FLOAT(2,1), Price FLOAT(2,1), Overall FLOAT(2,1))')
print("Table 2 created successfully")

conn.close()
