#!/usr/bin/python

import pygame
import math
import os
import sys
from pygame.locals import *
import artmanager

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

        #self.image, self.rect = load_png('mixtape.png')
        self.image, self.rect = load_png('tmp_user_art.png')
        self.height = self.rect.height
        self.width = self.rect.width

    def move(self):
        self.x += self.move_dist

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

        #init sound effect
        if _audio_enabled:
            self.fire_sound = pygame.mixer.Sound(load_wav('converted.wav'))



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
            if _audio_enabled:
                #self.fire_sound.stop() #Stop previous sound if there was one
                self.fire_sound.play(loops=0, maxtime=0) # "supa hot"



## Running the game

def main():
    global _audio_enabled

    #Prompt user for art
    artmanager.get_user_art()

    # misc data
    _height = 600
    _width = 900
    _player_height = 92
    _audio_enabled = False if '--disable-audio' in sys.argv else True

    # pre_init Pygame audio mixer
    if _audio_enabled:
        #pygame.mixer.pre_init(frequency=48000, size=-24, channels=2, \
        #        buffer=(2**20) )
        pygame.mixer.pre_init(frequency=22050, buffer=(2**20))

    # Initialise screen
    pygame.init()
    pygame.mixer.init()
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

    # Initialize text
    font = pygame.font.Font(None, 28)

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
        clock.tick(40) #cap at 60fps

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

        # prepare screen to be re-drawn
        screen.blit(background, (0, 0))

        # HUD
        # mixtapes remaining
        mixtapes_left = (10,10,10)
        no_mixtapes = (250,0,0)
        text = font.render("Mixtapes: {}".format(player.mixtapes_remaining), 1,
                mixtapes_left if player.mixtapes_remaining > 0 else no_mixtapes)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        screen.blit(text, textpos)

        # playersprite.update()
        player.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()

