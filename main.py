import pygame
import sys


def main():
	'''
	runs the main game loop and
	manages everything
	'''

	pygame.init()
	screen = pygame.display.set_mode((500, 500))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		pygame.display.flip()


if __name__ == "__main__":
	main()
