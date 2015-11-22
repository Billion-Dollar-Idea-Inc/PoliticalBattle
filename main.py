import pygame
import sys
import character
import crudder

class HomeScreen:
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 50)
		self.labeltitle1 = self.font.render("Political", 1, (255, 255, 255))
		self.labeltitle2 = self.font.render("Battle", 1, (255, 255, 255))
		self.font = pygame.font.SysFont("monospace", 30)
		self.labeldem = self.font.render("Democrat", 1, (0, 0, 0))
		self.labelrep = self.font.render("Republican", 1, (0, 0, 0))
		self.labelx = 160
		self.labely = 235
		self.background_color = (255, 255, 255)
		self.dem_color = (0, 0, 255)
		self.title_color = (0,0,0)
		self.demrectx = 100
		self.demrecty = 200
		self.demrectw = 300
		self.demrecth = 100
		self.rep_color = (255, 0, 0)
		self.reprectx = 100
		self.reprecty = 350
		self.reprectw = 300
		self.reprecth = 100
		self.is_dem = True


	def get_home_screen(self, screen):
		'''paints the home page to the screen'''
		screen.fill(self.background_color)
		background = pygame.image.load('images/start_back.jpg')
		screen.blit(background, [0, 0])
		pygame.draw.rect(screen, self.title_color, pygame.Rect(self.demrectx-20, self.demrecty-160, self.demrectw+40, self.demrecth+20))
		screen.blit(self.labeltitle1, (110, 50))
		screen.blit(self.labeltitle2, (175, 100))
		pygame.draw.rect(screen, self.dem_color, pygame.Rect(self.demrectx, self.demrecty, self.demrectw, self.demrecth))
		screen.blit(self.labeldem, (self.labelx + 20, self.labely))
		pygame.draw.rect(screen, self.rep_color, pygame.Rect(self.reprectx, self.reprecty, self.reprectw, self.reprecth))
		screen.blit(self.labelrep, (self.labelx, self.labely+140))
		return screen

	def is_in_dem_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.demrectx and xpos < self.demrectx+self.demrectw:
			if ypos > self.demrecty and ypos < self.demrecty+self.demrecth:
				return True
		return False

	def is_in_rep_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.reprectx and xpos < self.reprectx+self.reprectw:
			if ypos > self.reprecty and ypos < self.reprecty+self.reprecth:
				return True
		return False

class CharacterScreen():
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 15)

                self.crud = crudder.Crudder()

		#for layer above players char choice
		self.labelPlay = self.font.render("Player", 1, (255, 255, 255))
		self.labelPlayx = 75
		self.labelPlayy = 20
		#for label above opps char choice
		self.labelOpp = self.font.render("Opponent", 1, (255, 255, 255))
		self.labelOppx = 350
		self.labelOppy = 20
		#label and positions for start and back buttons
		self.labelBack = self.font.render("Back", 1, (255, 255, 255))
		self.labelStart = self.font.render("Start", 1, (255, 255, 255))
		self.labelBackx = 90
		self.labelStartx = 360
		self.labelStartBacky = 465
		#background and rectangle coloring
		self.background_color = (100, 100, 100)
		self.rect_color = (0, 0, 100)
		self.rect_color2 = (0, 100, 0)
		self.rect_color3 = (100, 0, 0)
		self.rect_color4 = (0, 0, 0)
		#rectangles where the choices will be listed
		self.rectPlayx = 20
		self.rectPlayy = 50
		self.rectOppx = 300
		self.rectOppy = 50
		#start and back button sizing/positioning
		self.rectStarth = 25
		self.rectStartw = 100
		self.rectStartx = 330
		self.rectStarty = 460
		self.rectBackx = 60
		#sizing of the choice list rects
		self.rectCharh = 400
		self.rectCharw = 180
		#sets the choice boxes variable
		self.PlaySelect = 0
		self.OppSelect = 0
		#if one game won you unlock obama and reagan
		self.unlock_players = False
		self.done = False

	def get_character_screen(self, screen):
		'''paints char screen to window'''
		self.loopInc = 0
		self.rectPlayChoicey = 60
		screen.fill(self.background_color)
		pygame.draw.rect(screen, self.rect_color2, pygame.Rect(self.rectStartx, self.rectStarty, self.rectStartw, self.rectStarth))
		pygame.draw.rect(screen, self.rect_color3, pygame.Rect(self.rectBackx, self.rectStarty, self.rectStartw, self.rectStarth))
		screen.blit(self.labelPlay, (self.labelPlayx, self.labelPlayy))
		screen.blit(self.labelStart, (self.labelStartx, self.labelStartBacky))
		screen.blit(self.labelOpp, (self.labelOppx, self.labelOppy))
		screen.blit(self.labelBack, (self.labelBackx, self.labelStartBacky))

                if self.party == "DEM":
                    self.nameList = self.crud.get_chars_in_party("DEM")
                else:
                    self.nameList = self.crud.get_chars_in_party("REP")

		for x in range(0, self.play_ops):
			if x == self.PlaySelect:
				pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rectPlayx, self.rectPlayy+(x*self.playh), self.optionw, self.playh))
                                self.nColor = (0, 0, 0)
			else:
                                self.nColor = (255, 255, 255)
                                if self.party == "DEM":
				    pygame.draw.rect(screen, (0, 0, 255 - (x * 30)), pygame.Rect(self.rectPlayx, self.rectPlayy+(x*self.playh), self.optionw, self.playh))
                                else:
				    pygame.draw.rect(screen, (255 - (x * 30), 0, 0), pygame.Rect(self.rectPlayx, self.rectPlayy+(x*self.playh), self.optionw, self.playh))
                        self.name = self.font.render(self.nameList[x], 1, self.nColor)
                        screen.blit(self.name, (self.rectPlayx + 10, self.rectPlayy + (x*self.playh) + self.playh/2 - 10))

                if self.party == "DEM":
                    self.nameList = self.crud.get_chars_in_party("REP")
                else:
                    self.nameList = self.crud.get_chars_in_party("DEM")

		for x in range(0, self.opp_ops):
			if x == self.OppSelect:
				pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rectOppx, self.rectOppy+(x*self.opph), self.optionw, self.opph))
                                self.nColor = (0, 0, 0)
			else:
                                self.nColor = (255, 255, 255)
                                if self.party != "DEM":
				    pygame.draw.rect(screen, (0, 0, 255-(x * 30)), pygame.Rect(self.rectOppx, self.rectOppy+(x*self.opph), self.optionw, self.opph))
                                else:
				    pygame.draw.rect(screen, (255 - (x * 30), 0, 0), pygame.Rect(self.rectOppx, self.rectOppy+(x*self.opph), self.optionw, self.opph))
                        self.name = self.font.render(self.nameList[x], 1, self.nColor)
                        screen.blit(self.name, (self.rectOppx + 10, self.rectOppy + (x*self.opph) + self.opph/2 - 10))
		return screen

	def unlock_player(self):
		self.unlock_players = True

	def set_party(self, party):
		self.party = party
		c = crudder.Crudder()
		self.play_ops = c.get_num_chars_in_party(party)
		if party == "DEM":
			self.opp_ops = c.get_num_chars_in_party("REP")
		else:
			self.opp_ops = c.get_num_chars_in_party("DEM")
		if not self.unlock_players:
			self.play_ops -=1
			self.opp_ops -=1
		self.optionw = self.rectCharw
		total = self.rectCharh
		self.playh = total/self.play_ops
		self.opph = total/self.opp_ops

	def is_in_start_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.rectStartx and xpos < self.rectStartx+self.rectStartw:
			if ypos > self.rectStarty and ypos < self.rectStarty+self.rectStarth:
				return True
		return False

	def is_in_back_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.rectBackx and xpos < self.rectBackx+self.rectStartw:
			if ypos > self.rectStarty and ypos < self.rectStarty+self.rectStarth:	
				return True
		return False

	def set_character(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		for x in range(0, self.play_ops):
			if xpos > self.rectPlayx and xpos < self.rectPlayx+self.optionw:
				if ypos > self.rectPlayy+(x*self.playh) and ypos < self.rectPlayy+(x*self.playh)+self.playh:
					self.PlaySelect = x

	   	for x in range(0, self.opp_ops):
	    		if xpos > self.rectOppx and xpos < self.rectOppx+self.optionw:
	    			if ypos > self.rectOppy+(x*self.opph) and ypos < self.rectOppy+(x*self.opph)+self.opph:
	    				self.OppSelect = x

	def reset_characters(self):
		self.PlaySelect = 0
		self.OppSelect = 0

	def get_chars_to_battle(self):
            '''
            Returns current selected Characters for player and oppenet,
            returned as a 2 item list with player in idex 0, opponent in 1
            '''
            repOptions = self.crud.get_chars_in_party("REP")
            demOptions = self.crud.get_chars_in_party("DEM")

            if self.party == "DEM":
                # print demOptions[self.PlaySelect], " ", repOptions[self.OppSelect]
                return (demOptions[self.PlaySelect], repOptions[self.OppSelect])
            if self.party == "REP":
                # print repOptions[self.PlaySelect], " ", demOptions[self.OppSelect]
                return (repOptions[self.PlaySelect], demOptions[self.OppSelect])

class GameScreen():
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 30)
		#four boxes for the attacks
		self.attboxesx = [0, 200, 0, 200]
		self.attboxesy = [300, 300, 400, 400]
		self.attboxesw = 200
		self.attboxesh = 100		
		#paramers for white background for play image
		self.bgroundc = (210,210,210)
		self.bgroundx = 0
		self.bgroundy = 190
		self.bgroundw = 110
		self.bgroundh = 110
		#paramers for white background for opp image	
		self.bgroundoppx = 390
		self.bgroundoppy = 0
		#box for the options box
		self.exboxx = 400
		self.exboxy = 400
		self.exboxw = 100
		self.exboxh = 100
		self.exboxc = (200, 200, 200)
		self.exboxn = (100, 100, 100)
		self.playimgx = 0
		self.playimgy = 200
		self.oppimgx = 400
		self.oppimgy = 0
        #labels
		self.eLabel = self.font.render("Exit", 1, (0, 0, 0))
		self.nLabel = self.font.render("Next", 1, (0, 0, 0))
		self.eLabelX = self.exboxx + 15
		self.eLabelY = self.exboxy + self.exboxh/2 - 15
		#booleans for gameplay control
		self.player_turn = True
		self.show_attack = False
		self.show_opp_attack = False
		self.opp_turn = False

	def set_players(self, names):
            	''' sets player and opponent for GameScreen to use and draw variables from'''
	    	self.player_turn = True
	    	self.player = character.Character(names[0])
	    	if self.player.get_party() == "DEM":
			self.attboxesc = [(0, 0, 125), (0, 0, 250), (0, 0, 250), (0, 0, 125)]
		else:
		     	self.attboxesc = [(125, 0, 0), (250, 0, 0), (250, 0, 0), (125, 0, 0)]
            	self.opponent = character.Character(names[1])

	def set_images(self, player, opponent):
		'''this function currently assumes that the images will be jpegs
		   so we will probably need to change that and we'll also need to
		   change it to reflect how the pictures are actually named'''

		self.playimg = pygame.image.load("images/" + self.player.get_picture_name("right"))
		self.playimg = pygame.transform.scale(self.playimg, (100, 100))
		self.oppimg = pygame.image.load("images/" + self.opponent.get_picture_name("left"))
		self.oppimg = pygame.transform.scale(self.oppimg, (100, 100))

	def set_attacks(self, player):
		c = crudder.Crudder()
		self.attacks = c.get_attacks(player.get_name())

	def set_descriptions(self, player):
		c = crudder.Crudder()
		self.descs = c.get_attack_descs(player.get_name())
	
	def set_power(self, player):
		c = crudder.Crudder()
		self.powers = c.get_attack_powers(player.get_name())

	def get_attack(self, pos):
		'''
		with buttons in layout:  1    2
					 3    4
		return the number of the attack button which was clicked, 1-4,
		or None if pos is not within any of them
		'''
		xpos = pos[0]
		ypos = pos[1]
		for x in range(0, 4):
			if xpos > self.attboxesx[x] and xpos < self.attboxesx[x]+self.attboxesw:
				if ypos > self.attboxesy[x] and ypos < self.attboxesy[x]+self.attboxesh:
					return x
		return None

	def display_health(self, screen):
		self.PlayerHealthBarY = 284
		self.PlayerHealthBarX = 100
		self.healthBarW = 15
		self.healthBarH = 100
		self.playHealthBarH = self.player.get_health()
		self.oppHealthBarH = self.opponent.get_health()
		self.OppHealthBarY = 0
		self.OppHealthBarX = 300
		#paints red bar underneath healthbar to indicate lost health
		pygame.draw.rect(screen, (200, 0, 0,), pygame.Rect(self.PlayerHealthBarX, self.PlayerHealthBarY, self.healthBarH, self.healthBarW))
		pygame.draw.rect(screen, (200, 0, 0,), pygame.Rect(self.OppHealthBarX, self.OppHealthBarY, self.healthBarH, self.healthBarW))
		#paints the actual healthbar
		if self.playHealthBarH > 0:
			pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.PlayerHealthBarX, self.PlayerHealthBarY, self.playHealthBarH, self.healthBarW))
		if self.oppHealthBarH > 0:	
			pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.OppHealthBarX, self.OppHealthBarY, self.oppHealthBarH, self.healthBarW))

	def is_exit_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.exboxx and xpos < self.exboxx + self.exboxw:
			if ypos > self.exboxy and ypos < self.exboxy + self.exboxh:
				return True
		return False

	def is_next_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.exboxx and xpos < self.exboxx + self.exboxw:
			if ypos > self.exboxy - self.exboxh and ypos < self.exboxy:
				return True
		return False

	def attack(self, attackPos):
		'''displays attack desc on the screen and decrements opp health'''
		if self.player_turn:
			self.currentAttack = self.player.get_attack_description(attackPos)#sets attack selected description to speaking bubble
			self.show_attack = True
			self.opponent.dec_health(self.powers[attackPos])
			self.player_turn = False
		else:
			self.oppAttack = self.opponent.get_random_attack()
			self.currentOppAttack = self.oppAttack[0]
			self.player.dec_health(self.oppAttack[1])
			self.show_opp_attack = True
			self.player_turn = True
	
	def render_text(self, screen, font, text, pos, color):
		'''using the parameters, draws rectangle to the screen with the
		   given text formatted to be multilined inside
		   pos = position of box (x, y)
		   rest is self explantory'''	
		text =  text.replace("\\n", "\n")
		lines = text.splitlines()  #splits lines into a list by \n's	
		width = 0
		height = 0
		for l in lines:   #determine total height of box maybe?  not sure this loop is mostly magic from internet
			width = max(width, font.size(l)[0])
			height += font.get_linesize()
		height = 0
		for l in lines:       #create the different lines and print each to the screen    
			t = font.render(l, 0, color)
			screen.blit(t, (pos[0], height + pos[1]))
			height += font.get_linesize()
		return screen

	def display_attack(self, screen, insult, isPlayer):
		'''Function needs screen to work, takes string that is the insult
		and true or false for isPlayer and displays in a speach bubble'''
		x = 100
		y = 100
		w = 320
		h = 100
		pygame.draw.ellipse(screen, (200, 200, 200), (x, y, w, h), 0)
		if isPlayer:
		    pygame.draw.polygon(screen, (200, 200, 200), [(self.playimgx + 80, self.playimgy + 20), (x + 25, y + h/2 - 2), (x + w/3 + 50, y + h/2 - 2), (self.playimgx + 80, self.playimgy + 20)], 0)
		else:
		    pygame.draw.polygon(screen, (200, 200, 200), [(self.oppimgx + 20, self.oppimgy + 80), (x + w - 25, y + h/2 -2), (x + 2*w/3 - 50, y + h/2 -2), (self.oppimgx + 20, self.oppimgy + 80)], 0)
		screen = self.render_text(screen, pygame.font.SysFont("monospace", 10), insult, (x + 25, y + h/2 - 10), (0, 0, 0))

	def clear_attack_bubble(self):
		'''clears text bubble in middle of screen'''
		self.show_attack = False
		self.show_opp_attack = False

	def in_screen(self,pos):
		'''if there is a mouse click in the screen'''
		xpos = pos[0]
		ypos = pos[1]
		if xpos > 0 and xpos < 500:
			if ypos > 0 and ypos < 500:
				return True
		return False


	def get_game_screen(self, screen):
		'''prints game screen to window'''
		screen.fill((255, 255, 255))
		background = pygame.image.load('images/char_back.jpg')
		screen.blit(background, [0, 0])
		pygame.draw.rect(screen, self.exboxc, pygame.Rect(self.exboxx, self.exboxy, self.exboxw, self.exboxh))#exit box
		screen.blit(self.eLabel, (self.eLabelX, self.eLabelY))
		pygame.draw.rect(screen, self.exboxn, pygame.Rect(self.exboxx, self.exboxy-self.exboxh, self.exboxw, self.exboxh))#'next' box 
		screen.blit(self.nLabel, (self.eLabelX, self.eLabelY-self.exboxh))
		pygame.draw.rect(screen, self.bgroundc, pygame.Rect(self.bgroundx, self.bgroundy, self.bgroundw, self.bgroundh))#white background behind player
		pygame.draw.rect(screen, self.bgroundc, pygame.Rect(self.bgroundoppx, self.bgroundoppy, self.bgroundw, self.bgroundh))#white bacground behind opp
		screen.blit(self.playimg, (self.playimgx, self.playimgy)) # display image for player
		screen.blit(self.oppimg, (self.oppimgx, self.oppimgy)) # display image for opponent		
		health = self.player.get_health()
		ohealth = self.opponent.get_health()
		if ohealth < 0:
			ohealth = 0
		if health < 0:
			health = 0
		health = str(health)+"hp"
		ohealth = str(ohealth)+"hp"
		self.hfont = pygame.font.SysFont("monospace", 15)
		self.Health = self.hfont.render(health, 1, (255, 255, 255))
		screen.blit(self.Health,(135,260))
		self.oppHealth = self.hfont.render(ohealth, 1, (255, 255, 255))
		screen.blit(self.oppHealth,(320,15))
		for x in range(0, 4):
			pygame.draw.rect(screen, self.attboxesc[x], pygame.Rect(self.attboxesx[x], self.attboxesy[x], self.attboxesw, self.attboxesh))
			fontSize = 15
			afont = pygame.font.SysFont("monospace", fontSize)
			att = self.attacks[x]
			screen = self.render_text(screen, afont, att, (self.attboxesx[x] + fontSize, self.attboxesy[x] + self.attboxesh/2 - fontSize), (255, 255, 255))
		if self.show_attack:
			self.display_attack(screen, self.currentAttack , True)
			self.player_turn = False
		elif self.show_opp_attack:
			self.display_attack(screen, self.currentOppAttack, False)
			self.player_turn = True
		self.display_health(screen)
		return screen

	def check_for_win(self):
		'''returns either win loss or False'''
		if self.player.get_health() < 1:
			return "loss"
		elif self.opponent.get_health() < 1:
		   	return "win"
		else:
		   	return False

class EndScreen():
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 30)
		self.font2 = pygame.font.SysFont("monospace", 20)
		self.font3 = pygame.font.SysFont("monospace", 15)
		#box for background of result
		self.resboxx = 180
		self.resboxy = 190
		self.resboxw = 150
		self.resboxh = 50
		self.resboxc = (200, 200, 200)
		self.resboxn = (100, 100, 100)
		self.imgx = 200
		self.imgy = 100
		self.unlocked = False

	def set_images(self, player, opponent):
		'''set opponent and player pictures to display winner'''
		self.playimg = pygame.image.load("images/" + player.get_picture_name("right"))
		self.playimg = pygame.transform.scale(self.playimg, (100, 100))
		self.oppimg = pygame.image.load("images/" + opponent.get_picture_name("left"))
		self.oppimg = pygame.transform.scale(self.oppimg, (100, 100))
		self.playname = player.get_name()
		self.oppname = opponent.get_name()

	def get_end_screen(self, screen, res, bonus):
		'''prints end screen to window'''
		screen.fill((255, 255, 255))
		background = pygame.image.load('images/flag.jpg')
		screen.blit(background, [0, 0])
		pygame.draw.rect(screen, self.resboxc, pygame.Rect(self.resboxx, self.resboxy, self.resboxw, self.resboxh))	
		result = self.font.render("Winner:", 1, (0, 0, 0))
		if res == "win":
			name = self.font.render(self.playname, 1, (255, 255, 255))
			screen.blit(self.playimg, (self.imgx, self.imgy))
		elif res == "loss":
			name = self.font.render(self.oppname, 1, (255, 255, 255))
			screen.blit(self.oppimg, (self.imgx, self.imgy))
		screen.blit(result, (200, 200))
		screen.blit(name, (150, 250))		
		end = self.font2.render("Click anywhere to exit", 1, (255, 255, 255))	
		screen.blit(end, (110, 300))

		if bonus:
			unlock = self.font3.render("Bonus players unlocked!", 1, (255, 255, 255))	
			screen.blit(unlock, (110, 350))
			players = self.font3.render("Barack Obama and Ronald Reagan", 1, (255, 255, 255))	
			screen.blit(players, (110, 400))
		return screen

def main():
	'''
	runs the main game loop and
	manages everything
	'''

	pygame.init()
	screen = pygame.display.set_mode((500, 500))

	hs = HomeScreen()
	cs = CharacterScreen()
	gs = GameScreen()
	es = EndScreen()
	unlock = False
	bonus = False

	#TODO:
	#resize attack names if they are too big

	game_state = 1

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game_state == 1:
					cs.reset_characters()
					if hs.is_in_dem_button(pygame.mouse.get_pos()):
						game_state = 2
						cs.set_party("DEM")
					if hs.is_in_rep_button(pygame.mouse.get_pos()):
						game_state = 2
						cs.set_party("REP")
				elif game_state == 2:
				  	if cs.is_in_start_button(pygame.mouse.get_pos()):
						game_state = 3
						gs.set_players(cs.get_chars_to_battle())
						gs.set_images(gs.player,gs.opponent)
						gs.set_attacks(gs.player)
						gs.set_descriptions(gs.player)
						gs.set_power(gs.player)
					elif cs.is_in_back_button(pygame.mouse.get_pos()):
						game_state = 1
					else:
						cs.set_character(pygame.mouse.get_pos())
				elif game_state == 3:
					if gs.check_for_win() != False and  (gs.in_screen(pygame.mouse.get_pos())):#if game is over and user makes an additional click 
						if gs.check_for_win() == "win" and not unlock:
							cs.unlock_player()
							unlock = True
							bonus = True
						else:
							bonus = False
						game_state = 4	
						gs.clear_attack_bubble()
						es.set_images(gs.player,gs.opponent)
						result = gs.check_for_win()#sets result to win or loss
					elif not gs.player_turn and gs.is_next_button(pygame.mouse.get_pos()):
						gs.clear_attack_bubble()
						gs.attack(gs.get_attack(pygame.mouse.get_pos()))
					elif gs.is_next_button(pygame.mouse.get_pos()):
						gs.clear_attack_bubble()
					elif gs.get_attack(pygame.mouse.get_pos()) != None:#if it is player turn text bubble is cleared and it waits for player attack
						gs.clear_attack_bubble()
						gs.attack(gs.get_attack(pygame.mouse.get_pos()))
					elif gs.is_exit_button(pygame.mouse.get_pos()):
						gs.clear_attack_bubble()
						game_state = 1	
				elif game_state == 4:
					if gs.in_screen(pygame.mouse.get_pos()):#checks to see if anywhere is clicked
						game_state = 1

		if game_state == 1:
		 	screen = hs.get_home_screen(screen)
		elif game_state == 2:
		 	screen = cs.get_character_screen(screen)
		elif game_state == 3:
			screen = gs.get_game_screen(screen)
		elif game_state == 4:
			screen = es.get_end_screen(screen, result, bonus)
		pygame.display.update()
		pygame.display.flip()

if __name__ == "__main__":
	main()
