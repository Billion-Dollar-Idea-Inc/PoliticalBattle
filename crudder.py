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
		'''return health of player'''
		sub = name[0:5]
		self.c.execute("SELECT health FROM people WHERE name LIKE \"{subs}%\""\
				.format(subs = sub))
		health = self.c.fetchall()
		health = health[0][0]
		return health

	def get_attacks(self, name):
		'''return list of attack names in order'''
		sub = name[0:5]
		self.c.execute("SELECT attack FROM attacks WHERE name LIKE \"{subs}%\""\
				.format(subs = sub))
		attacks = self.c.fetchall()
		return attacks # I hope this works

	def get_attack_descs(self, name):
                '''return attack descriptions'''
                sub = name[0:5]
		self.c.execute("SELECT desc FROM attacks WHERE name LIKE \"{subs}%\""\
				.format(subs = sub))
		descs = self.c.fetchall()
		return descs

	def get_attack_powers(self, name):
		'''return a dictionary of attacks with their powers'''
		sub = name[0:5]
		self.c.execute("SELECT power FROM attacks WHERE name LIKE \"{subs}%\""\
				.format(subs = sub))
		powers = self.c.fetchall()
		return powers 

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
