import pygame
import sys


class HomeScreen:
	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 30)
		self.label = self.font.render("Start", 1, (0, 0, 0))
		self.labelx = 150
		self.labely = 250
		self.background_color = (255, 255, 255)
		self.rectx = 100
		self.recty = 200
		self.rectw = 300
		self.recth = 100
		self.rect_color = (100, 100, 100)
		pass

	def get_home_screen(self, screen):
		'''paints the home page to the screen'''
		screen.fill(self.background_color)
		pygame.draw.rect(screen, self.rect_color, pygame.Rect(self.rectx, self.recty, self.rectw, self.recth))
		screen.blit(self.label, (self.labelx, self.labely))
		return screen

	def is_in_start_button(self, pos):
		xpos = pos[0]
		ypos = pos[1]
		if xpos > self.rectx and xpos < self.rectx+self.rectw:
			if ypos > self.recty and ypos < self.recty+self.recth:
				return True
		return False

class CharacterSelect():
	def __init__():
		pass

	

def main():
	'''
	runs the main game loop and
	manages everything
	'''

	pygame.init()
	screen = pygame.display.set_mode((500, 500))

	hs = HomeScreen()

	# -- this would need to be worked out --
	#if 1, then were at the home screen
	#if 2, were at character selection
	#if 3, in the game?
	game_state = 1

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game_state == 1:
					if hs.is_in_start_button(pygame.mouse.get_pos()):
						game_state = 2
		if game_state == 1:
		 	screen = hs.get_home_screen(screen)
		elif game_state == 2:
		 	screen = cs.get_char_select_screen(screen)
		pygame.display.update()
		pygame.display.flip()


if __name__ == "__main__":
	main()
