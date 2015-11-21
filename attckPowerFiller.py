import random
import sqlite3
import crudder

#still needs to be tested, then ran


crud = crudder.Crudder()
conn = sqlite3.connect("data.db")
c = self.conn.cursor()

names = crud.get_chars_in_party("DEM") + crud.get_chars_in_party("REP")
for name in names:
	num = random.randint(10, 30)
	c.execute("UPDATE attacks SET power = {_num} WHERE name LIKE {_name}".format(_num = num, _name = name[0:5]))
