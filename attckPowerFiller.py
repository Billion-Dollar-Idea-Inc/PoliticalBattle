import random
import sqlite3
import crudder

crud = crudder.Crudder()
conn = sqlite3.connect("try.db")
c = conn.cursor()

names = crud.get_chars_in_party("DEM") + crud.get_chars_in_party("REP")
for name in names:
	attacks = crud.get_attacks(name)
	for attack in attacks:
		num = int(random.randint(10, 40))
		c.execute("UPDATE attacks SET power = 30 WHERE attack = \"{rattack}\"".format(rattack = attack))
