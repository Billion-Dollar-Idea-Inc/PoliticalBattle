import crudder
import random

class Character(object):
	def __init__(self, name):
		self.name = name
		self.c = crudder.Crudder()
		self.orig_health = self.c.get_health(name)
		self.health = self.c.get_health(name)
		self.party = self.c.get_party(name)
		self.attacks = self.c.get_attacks(name)
		self.attack_powers = self.c.get_attack_powers(name)
		self.attack_descs = self.c.get_attack_descs(name)

	def add_attack(self, attack):
		'''
		add an attack to the character's
		list of attacks
		'''
		if attack not in attacks:
			self.attacks.append(attack)

	def add_attacks(self, attacks):
		'''
		add multiple attacks to the character's
		list of attacks
		'''
		for attack in attacks:
			if attack not in attacks:
				self.attacks.append(attack)

	def add_health(self, amount):
		'''increase health'''
		self.health = self.health + amount

	def dec_health(self, amount):
		'''decrease health'''
		self.health = self.health - amount

	def get_health(self):
		'''return health'''
		return self.health

	def reset_health(self):
		'''reset health back to original value'''
		self.health = self.orig_health

	def get_attacks(self):
		'''returns list of attacks'''
		return self.attacks

	def get_name(self):
		'''returns name'''
		return self.name

	def get_attack_description(self, attack):
		'''returns attack description given attack name'''
		desc = self.attack_descs[attack]
                return desc

	def get_attack_power(self, attack):
		'''returns power of attack'''
		return self.attack_power[attack]

	def get_party(self):
		'''returns party affiliation, either REP or DEM'''
		return self.party

	def get_random_attack(self):
		'''returns random attack in an array of side two with name and power'''
		rand = random.randint(0, len(self.attacks)-1)
		desc = self.attack_descs[rand]
		power = self.attack_powers[rand]
		return [desc, power]
	
	def get_picture_name(self, direction):
		'''returns player picture'''
		fileName = self.name[self.name.find(" ",0) + 1:]
		fileName = fileName + "_" + direction + ".jpg"
		fileName = fileName.lower()
		return fileName
