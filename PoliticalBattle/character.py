class Character(object):
	def __init__(self, name):
		self.name = name
		self.attacks = []

	def add_attack(self, attack):
		'''
		add an attack to the character's
		list of attacks
		'''
		self.attacks.append(attack)

	def add_attacks(self, attacks):
		'''
		add multiple attacks to the character's
		list of attacks
		'''
		for attack in attacks:
			if attack not in attacks:
				self.attacks.append(attack)

	def get_attacks(self):
		'''returns list of attacks'''
		return self.attacks

	def get_name(self):
		'''returns name'''
		return self.name
