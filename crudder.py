import sqlite3

'''
Manages the interaction between the program
and the database suing SQLite3
'''
class Crudder():
	def __init__(self):
		self.conn = sqlite3.connect("data.db")
		self.conn.text_factory = str
		self.c = self.conn.cursor()

	def get_health(self, name):
		sub = name[0:5]
		self.c.execute("SELECT health FROM people WHERE name LIKE \"{subs}%\""\
				.format(subs = sub))
		health = self.c.fetchall()
		health = health[0][0]
		return health

	def get_attacks(self, name):
		pass

	def get_attack_descs(self, name):
		pass

	def get_attack_powers(self, name):
		pass

	def get_party(self, name):
		sub = name[0:5]
		self.c.execute("SELECT party FROM people WHERE name LIKE \"{subs}%\""\
			.format(subs = sub))
		party = self.c.fetchall()
		party = party[0][0]
		return party

	def get_num_chars_in_party(self, party):
		if party == "DEM" or party == "REP":
			self.c.execute("SELECT COUNT(*) FROM people WHERE party = \"{_party}\""\
				.format(_party = party))
			fetch = self.c.fetchall()
			fetch = fetch[0][0]
			return int(fetch)
		else:
			return 0

	def get_chars_in_party(self, party):
		self.c.execute("SELECT name FROM people WHERE party = \"{_party}\""\
			.format(_party = party))
		fetch = self.c.fetchall()
		names = []
		for arr in fetch:
			names.append(arr[0])
		return names
