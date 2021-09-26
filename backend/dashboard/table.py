import sqlite3

connection_obj = sqlite3.connect('plants.db')

cursor_obj = connection_obj.cursor()

cursor_obj.execute("DROP TABLE IF EXISTS plants")

table = """ CREATE TABLE plants (
			Cname VARCHAR(25) NOT NULL,
			Bname CHAR(25) NOT NULL,
			discription CHAR(255),
			height varchar(50),
            img varchar(200)
		); """

cursor_obj.execute(table)

print("Table is Ready")

connection_obj.close()
