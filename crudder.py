import sqlite3

'''
Manages the interaction between the program
and the database. Appended from crudder.py
in project github.com/Derrreks/CRUD
'''
class Crudder():
	def __init__(self):
		self.conn = sqlite3.connect("data.db")
		self.conn.text_factory = str
		self.c = self.conn.cursor()

	def get_health(self, name):
		pass

	def get_attacks(self, name):
		pass

	def get_attack_descs(self, name):
		pass

	def get_attack_powers(self, name):
		pass

	def get_party(self, name):
		self.c.execute("SELECT party FROM people WHERE name = {_name}"\
			.format(_name = name))
		return self.c.fetchall()

	def get_num_chars_in_party(self, party):
		pass
