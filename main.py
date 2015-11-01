import pygame
import sys


'''
I'm not 100% sure on how to organize this and
how the game state should be managed so if you
think there's a better way do that
'''

#TODO
#in here will be hard coded all of the drawings
#to the home screen
def home_screen(screen):
	'''paints the home page to the screen'''
	return screen

#TODO
#just like above, self explanatory
def char_select_screen(screen):
	'''paints the char selection screen page to the screen'''
	return screen

def main():
	'''
	runs the main game loop and
	manages everything
	'''

	pygame.init()
	screen = pygame.display.set_mode((500, 500))

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
				''' in here if they like click on a certain
				button or something move to char select screen
				and set game _state to 2
				'''
		if game_state == 1:
		 	screen = home_screen(screen)
		elif game_state == 2:
		 	screen = char_select_screen(screen)
		pygame.display.update()
		pygame.display.flip()


if __name__ == "__main__":
	main()
