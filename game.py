#!/usr/bin/python

import pygame
import math
import os
from pygame.locals import *

## Util functions

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()

def load_wav(name):
    """ Load sound file and return object """    
    fullname = os.path.join('data', name)
    return fullname



## Objects
class mixtape_obj(pygame.sprite.Sprite):

    move_dist = 15

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        # info about image
        self.image, self.rect = load_png('mixtape.png')
        self.height = self.rect.height
        self.width = self.rect.width

        #sound effect
        self.superhot = pygame.mixer.Sound(load_wav('superhot.wav'))

    def move(self):
        self.x += self.move_dist
        self.superhot.play(loops=0, maxtime=0) #play sound effect
        self.superhot.stop()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class player_obj(pygame.sprite.Sprite):

    move_dist = 10

    def __init__(self, x, y, level=1):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        # info about image
        self.image, self.rect = load_png('player.png')
        self.height = self.rect.height
        self.width = self.rect.width


        # info about environment
        screen = pygame.display.get_surface()
        self.max_height = screen.get_height()
        self.max_width = screen.get_width()
        self.area = screen.get_rect()

        # mixtape info
        self.mixtapes = []
        self.mixtapes_remaining = level * 12


    def moveup(self):
        if self.y >= self.move_dist:
            self.y -= self.move_dist
        else:
            self.y = 0

    def movedown(self):
        if self.y <= self.max_height - (self.height + self.move_dist):
            self.y += self.move_dist
        else:
            self.y = self.max_height - self.height

    def moveright(self):
        if self.x <= self.max_width/2:
            self.x += self.move_dist

    def moveleft(self):
        if self.x >= self.move_dist:
            self.x -= self.move_dist

    def movemixtapes(self):
        for tape in self.mixtapes:
            tape.move()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        for tape in self.mixtapes:
            surface.blit(tape.image, (tape.x, tape.y))

    def fire(self):
        if self.mixtapes_remaining > 0:
            b = mixtape_obj(self.x + self.width, self.y + self.height/3)
            self.mixtapes.append(b)
            self.mixtapes_remaining -= 1



## Running the game

def main():

    # misc data
    _height = 600
    _width = 900
    _player_height = 92

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((_width, _height))
    pygame.display.set_caption('StraightFire')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialize player
    player = player_obj(0, _height - _player_height)

    # Initialize sprites
    playersprite = pygame.sprite.RenderPlain((player))

    # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize clock
    clock = pygame.time.Clock()
    moveup = False
    movedown = False
    moveright = False
    moveleft = False

    # Event loop
    while 1:
        clock.tick(60) #cap at 60fps

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    moveup= True
                if event.key == K_DOWN:
                    movedown= True
                if event.key == K_RIGHT:
                    moveright = True
                if event.key == K_LEFT:
                    moveleft = True
                if event.key == K_SPACE:
                    player.fire()
            elif event.type == KEYUP:
                if event.key == K_UP:
                    moveup = False
                if event.key == K_DOWN:
                    movedown= False
                if event.key == K_RIGHT:
                    moveright = False
                if event.key == K_LEFT:
                    moveleft = False


        player.moveup() if moveup else None
        player.movedown() if movedown else None
        player.moveright() if moveright else None
        player.moveleft() if moveleft else None
        player.movemixtapes()

        screen.blit(background, (0, 0))
        playersprite.update()
        player.draw(screen)
        # playersprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()

