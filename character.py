class Character(object):
	def __init__(self, name):#variabel to intialize: health, party, attack, attack_description,
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
	
	def get_health(self):
                 '''returns health'''
                 return self.health

	def add_health(self, boost):
                 '''increases health'''
                 self.health += boost

	def lose_health(self, lose):
                '''decreases health'''
                self.health -= lose

	def get_attack_description(self, attack):
               '''retrieve description of attack'''
                pass

	def get_party(self):
               '''returns party affiliation'''
               return self.party

	def get_random_attack(self):
               '''return random attack'''
                rand  = random.randint(0,len(attacks))
		name = attack[rand]
		power = dict[name]
		toreturn = []
		toreturn.append(name)
		toreturn.append(power)
		return toreturn 

	def get_picture(self):
               '''returns player picture'''
               return self.image
