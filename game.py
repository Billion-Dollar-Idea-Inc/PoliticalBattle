#!/usr/bin/python

import pygame
import math
import os
import sys
import random
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
class enemy_obj(pygame.sprite.Sprite):

    move_dist = 12

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.x = x
        # self.y = y

        # info about image
        self.image, self.rect = load_png('hater.png')
        self.fire, self.fire_rect = load_png('fire.png')
        self.height = self.rect.height
        self.width = self.rect.width
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.on_fire = -1

    def move(self):
        if self.on_fire is -1:
            self.x -= self.move_dist
            self.rect.x -= self.move_dist


    def draw(self, surface):
        # surface.blit(self.image, (self.x, self.y))
        surface.blit(self.image, self.rect)
        if self.on_fire != -1:
            surface.blit(self.fire, self.rect)

class mixtape_obj(pygame.sprite.Sprite):

    move_dist = 15

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # info about image
        self.image, self.rect = load_png('tmp_user_art.png')
        #self.image, self.rect = load_png('mixtape.png')
        self.rect.left = x
        self.rect.top = y
        self.height = self.rect.height
        self.width = self.rect.width
        self.consumed = False

    def move(self):
        self.rect.left += self.move_dist

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class player_obj(pygame.sprite.Sprite):

    move_dist = 10

    def __init__(self, x, y, level=1):
        pygame.sprite.Sprite.__init__(self)

        # info about image
        self.image, self.rect = load_png('player.png')
        self.height = self.rect.height
        self.width = self.rect.width
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y


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
            self.fire_sound = pygame.mixer.Sound(load_wav('superhot.wav'))



    def move_up(self):
        if self.y >= self.move_dist:
            self.rect.y -= self.move_dist
            self.y -= self.move_dist
        else:
            self.rect.y = 0
            self.y = 0

    def move_down(self):
        if self.y <= self.max_height - (self.height + self.move_dist):
            self.rect.y += self.move_dist
            self.y += self.move_dist
        else:
            self.rect.y = self.max_height - self.height
            self.y = self.max_height - self.height

    def move_right(self):
        if self.x <= 3*self.max_width/5:
            self.rect.x += self.move_dist
            self.x += self.move_dist

    def move_left(self):
        if self.x >= self.move_dist:
            self.rect.x -= self.move_dist
            self.x -= self.move_dist

    def move_mixtapes(self):
        for tape in self.mixtapes:
            tape.move()
        mixtapes = [m for m in self.mixtapes if m.rect.x < self.max_width]

    def draw(self, surface):
        # surface.blit(self.image, (self.x, self.y))
        surface.blit(self.image, self.rect)
        for tape in self.mixtapes:
            tape.draw(surface)

    def fire(self):
        if self.mixtapes_remaining > 0:
            b = mixtape_obj(self.x + self.width, self.y + self.height/3)
            self.mixtapes.append(b)
            self.mixtapes_remaining -= 1
            if _audio_enabled:
                #self.fire_sound.stop() #Stop previous sound if there was one
                self.fire_sound.play(loops=0, maxtime=0) # "supa hot"

    def check_collisions(self, enemies):
        alive_enemies = [e for e in enemies if e.on_fire is -1]
        for tape in self.mixtapes:
            for e in alive_enemies:
                if tape.rect.colliderect(e.rect):
                    e.on_fire = 5
                    print "Hit!"
                    tape.consumed = True
        self.mixtapes = [m for m in self.mixtapes if not m.consumed]
        alive_enemies = [e for e in alive_enemies if e.on_fire is -1]
        return self.rect.collidelist(alive_enemies) != -1


## Running the game

def main():
    global _audio_enabled

    #Prompt user for art
    artmanager.get_user_art()

    # misc data
    _height = 720
    _width = 1360
    _player_height = 92
    _audio_enabled = False if '--disable-audio' in sys.argv else True

    # pre_init Pygame audio mixer
    if _audio_enabled:
        pygame.mixer.pre_init(frequency=22050, buffer=(2**20))

    # Initialise screen
    pygame.init()
    pygame.mixer.init()
    #Background music
    pygame.mixer.music.load(os.path.join('data', 'rickrosslow.ogg'))
    pygame.mixer.music.play(loops=-1)
    #pygame.mixer.music.set_volume(0.1)

    _level = 1

    # Initialise screen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, 0)
    print screen.get_size()
    pygame.display.set_caption('StraightFire')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialize player
    player = player_obj(0, _height - _player_height, _level)

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
    pygame.time.set_timer(USEREVENT+1, 1500)

    haters = []

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
            elif event.type == USEREVENT+1:
                enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,15))
                haters.append(enemy)


        player.move_up() if moveup else None
        player.move_down() if movedown else None
        player.move_right() if moveright else None
        player.move_left() if moveleft else None
        player.move_mixtapes()
        haters = [h for h in haters if h.x > -_player_height]
        for h in haters:
            h.move()
        if player.check_collisions(haters):
            print "Collision"
            break

        # prepare screen to be re-drawn
        screen.blit(background, (0, 0))

        # HUD
        # mixtapes remaining
        mixtapes_left = (10,10,10)
        no_mixtapes = (250,0,0)
        text = font.render("Level: {}   Mixtapes: {}".format(_level, player.mixtapes_remaining), 1,
                mixtapes_left if player.mixtapes_remaining > 0 else no_mixtapes)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        screen.blit(text, textpos)

        # playersprite.update()
        player.draw(screen)
        for h in haters:
            h.draw(screen)
        pygame.display.flip()

    print "You lose"

if __name__ == '__main__': main()

