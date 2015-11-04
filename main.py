import pygame
import sys

import crudder

class HomeScreen:
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 30)
		self.labeldem = self.font.render("Democrat", 1, (0, 0, 0))
		self.labelrep = self.font.render("Republican", 1, (0, 0, 0))
		self.labelx = 150
		self.labely = 250
		self.background_color = (255, 255, 255)
		self.demrectx = 100
		self.demrecty = 200
		self.demrectw = 300
		self.demrecth = 100
		self.rect_color = (100, 100, 100)
		self.reprectx = 100
		self.reprecty = 350
		self.reprectw = 300
		self.reprecth = 100
		self.is_dem = True

	def get_home_screen(self, screen):
		'''paints the home page to the screen'''
		screen.fill(self.background_color)
		pygame.draw.rect(screen, self.rect_color, pygame.Rect(self.demrectx, self.demrecty, self.demrectw, self.demrecth))
		screen.blit(self.labeldem, (self.labelx, self.labely))
		pygame.draw.rect(screen, self.rect_color, pygame.Rect(self.reprectx, self.reprecty, self.reprectw, self.reprecth))
		screen.blit(self.labelrep, (self.labelx, self.labely+100))
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
		
		#for layer above players char choice
		self.labelPlay = self.font.render("Player", 1, (0, 0, 0))
		self.labelPlayx = 75
		self.labelPlayy = 20
		#for label above opps char choice
		self.labelOpp = self.font.render("Opponent", 1, (0, 0, 0))
		self.labelOppx = 350
		self.labelOppy = 20
		#label and positions for start and back buttons
		self.labelBack = self.font.render("Back", 1, (255, 255, 255))
		self.labelStart = self.font.render("Start", 1, (255, 255, 255))
		self.labelBackx = 90
		self.labelStartx = 360
		self.labelStartBacky = 465
		#background and rectangle coloring
		self.background_color = (255, 255, 255)
		self.rect_color = (0, 0, 100)
		self.rect_color2 = (0, 100, 0)
		self.rect_color3 = (100, 0, 0)
		self.rect_color4 = (0, 0, 0)
		#rectangles where the choices will be listed
		self.rectPlayx = 10
		self.rectPlayy = 50
		self.rectOppx = 280
		self.rectOppy = 50
		#start and back button sizing/positioning
		self.rectStarth = 25
		self.rectStartw = 100
		self.rectStartx = 330
		self.rectStarty = 460
		self.rectBackx = 60
		#sizing of the choice list rects
		self.rectCharh = 400
		self.rectCharw = 200
		#sizing and positioning of player and opp choices
		self.rectChoiceh = 80
		self.rectChoicew = 160
		self.rectPlayChoicex = 30
		self.rectPlayChoicey = 60
		self.rectOppChoicex = 300
	
	def get_character_screen(self, screen):
		'''paints char screen to window'''
		self.loopInc = 0
		self.rectPlayChoicey = 60
		screen.fill(self.background_color)
		pygame.draw.rect(screen, self.rect_color, pygame.Rect(self.rectPlayx, self.rectPlayy, self.rectCharw, self.rectCharh))
		pygame.draw.rect(screen, self.rect_color, pygame.Rect(self.rectOppx, self.rectOppy, self.rectCharw, self.rectCharh))		
		pygame.draw.rect(screen, self.rect_color2, pygame.Rect(self.rectStartx, self.rectStarty, self.rectStartw, self.rectStarth))		
		pygame.draw.rect(screen, self.rect_color3, pygame.Rect(self.rectBackx, self.rectStarty, self.rectStartw, self.rectStarth))		
		pygame.draw.rect(screen, self.rect_color3, pygame.Rect(self.rectBackx, self.rectStarty, self.rectStartw, self.rectStarth))
		screen.blit(self.labelPlay, (self.labelPlayx, self.labelPlayy))
		screen.blit(self.labelStart, (self.labelStartx, self.labelStartBacky))
		screen.blit(self.labelOpp, (self.labelOppx, self.labelOppy))
		screen.blit(self.labelBack, (self.labelBackx, self.labelStartBacky))
		return screen

	def set_party(self, party):
		self.party = party
		c = crudder.Crudder()
		self.play_ops = c.get_num_chars_in_party(party)
		if party == "DEM":
			self.opp_ops = c.get_num_chars_in_party("REP")
		else:
			self.opp_ops = c.get_num_chars_in_party("DEM")
		#TODO
		#SET UP BOXES FOR THE CHOICES

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


class GameScreen():
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 30)
		#four boxes for the attacks
		self.attboxesx = [0, 200, 0, 200]
		self.attboxesy = [300, 300, 400, 400]
		self.attboxesw = 200
		self.attboxesh = 100
		#box for the options box
		self.exboxx = 400
		self.exboxy = 400
		self.exboxw = 100
		self.exboxh = 100
		self.exboxc = (200, 200, 200)
		
		self.playimgx = 0
		self.playimgy = 300
		self.oppimgx = 400
		self.oppimgy = 0
	
	def set_players(self, player, opponent):
		self.set_images(player, opponent)
		self.set_attacks(player)

	def set_images(self, player, opponent):
		'''this function currently assumes that the images will be jpegs
		   so we will probably need to change that and we'll also need to
		   change it to reflect how the pictures are actually named'''
		self.playimg = pygame.image.load("images/{play}.jpg"\
			.format(play = player))
		self.oppimg = pygame.images.load("images/{opp}.jpg"\
			.format(opp = opponent))

	def set_attacks(self, player):
		self.c = crudder.Crudder()
		attacks = c.get_attacks(player)

	def is_attack(self, pos):
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

	def is_exit_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.exboxx and xpos < self.exboxx + self.exboxw:
			if ypos > self.exboxy and ypos < self.exboxy + self.exboxh:
				return True
		return False

	def get_game_screen(self, screen):
		screen.fill((255, 255, 255))
		#screen.blit(self.playimg, (playimgx, playimgy))
		#screen.blit(self.oppimg, (oppimgx, oppimgy))
		pygame.draw.rect(screen, self.exboxc, pygame.Rect(self.exboxx, self.exboxy, self.exboxw, self.exboxh))
		for x in range(0, 4):
			pygame.draw.rect(screen, (0, 50*(x), 50), pygame.Rect(self.attboxesx[x], self.attboxesy[x], self.attboxesw, self.attboxesh))
		#print attack names to screen
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

	# -- this would need to be worked out --
	#if 1, then were at the home screen
	#if 2, were at character selection
	#if 3, in the game
	game_state = 1

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game_state == 1:
					if hs.is_in_dem_button(pygame.mouse.get_pos()):
						game_state = 2
						cs.set_party("DEM")
					if hs.is_in_rep_button(pygame.mouse.get_pos()):
						game_state = 2
						cs.set_party("REP")
				elif game_state == 2:
				  	if cs.is_in_start_button(pygame.mouse.get_pos()):
						game_state = 3
					elif cs.is_in_back_button(pygame.mouse.get_pos()):
						game_state = 1
				elif game_state == 3:
				  	if gs.is_attack(pygame.mouse.get_pos()) != None:
				  		#they clicked an attack
				  		pass
					elif gs.is_exit_button(pygame.mouse.get_pos()):
						game_state = 1
		if game_state == 1:
		 	screen = hs.get_home_screen(screen)
		elif game_state == 2:
		 	screen = cs.get_character_screen(screen)
		elif game_state == 3:
		    	screen = gs.get_game_screen(screen)
		pygame.display.update()
		pygame.display.flip()


if __name__ == "__main__":
	main()
