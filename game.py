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

    move_dist = 10

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
        else:
            self.on_fire -= 1


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

    move_dist = 8

    def __init__(self, x, y, level=1):
        pygame.sprite.Sprite.__init__(self)

        # info about image
        self.image, self.rect = load_png('player_new.png')
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
        self.level = 1
        self.mixtapes = []
        self.mixtapes_remaining = 4 + (self.level * 3)

        #init sound effect
        if _audio_enabled:
            self.fire_sound = pygame.mixer.Sound(load_wav('superhot.wav'))

    def levelup(self):
        self.level += 1
        self.mixtapes_remaining += 4 + (self.level * 2)

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

    def taunt(self):
        # play taunt noise
        print "Taunt"

    def check_hits(self, enemies):
        hit_count = 0
        alive_enemies = [e for e in enemies if e.on_fire is -1]
        for tape in self.mixtapes:
            for e in alive_enemies:
                if tape.rect.colliderect(e.rect):
                    e.on_fire = 25
                    tape.consumed = True
                    hit_count += 1
        self.mixtapes = [m for m in self.mixtapes if not m.consumed]
        return hit_count

    def check_collisions(self, enemies):
        alive_enemies = [e for e in enemies if e.on_fire is -1]
        return self.rect.collidelist(alive_enemies) != -1


## Running the game
def main():
    global _audio_enabled

    # Prompt user for art
    # artmanager.get_user_art()

    # misc data
    _player_height = 92
    _audio_enabled = False if '--disable-audio' in sys.argv else True

    # pre_init Pygame audio mixer
    if _audio_enabled:
        pygame.mixer.pre_init(frequency=22050, buffer=(2**20))

    pygame.init()
    pygame.mixer.init()
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

    #Background music
    pygame.mixer.music.load(os.path.join('data', 'rickrosslow.ogg'))
    pygame.mixer.music.play(-1)

    # Initialise screen
    pygame.display.set_caption('StraightFire')
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, 0)
    screen = pygame.display.set_mode((0,0))
    (_width, _height) = screen.get_size()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialize player
    player = player_obj(0, (_height - _player_height) / 2, 1)

    # Initialize sprites
    playersprite = pygame.sprite.RenderPlain((player))

    # Initialize text
    font = pygame.font.Font(None, 28)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize clock
    clock = pygame.time.Clock()

    # movement vars
    enemy_timer = 1200
    pygame.time.set_timer(USEREVENT+1, enemy_timer)
    moveup, upkey       = False, False
    movedown, downkey   = False, False
    moveright, rightkey = False, False
    moveleft, leftkey   = False, False
    haters = []

    # game stats
    level = 1
    hit_count = 0
    enemy_count = 0
    current_enemy_count = 0
    enemy_cap = 10
    

    # controller vars
    enable_360 = True
    # enable_360 = False
    fire_enabled = True
    taunt_enabled = True

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    xbox = joysticks[0]
    xbox.init()


    # Event loop
    while 1:
        clock.tick(60) #cap at 60fps

        # read controller input
        if enable_360:
            # A: fire mixtape
            fire_state = xbox.get_button(0)
            if fire_enabled and fire_state:
                player.fire()
                fire_enabled = False
            elif not fire_state:
                fire_enabled = True

            # B: taunt enemies
            taunt_state = xbox.get_button(1)
            if taunt_enabled and taunt_state:
                player.taunt()
                taunt_enabled = False
            elif not taunt_state:
                taunt_enabled = True

            # joystick movement
            joystick_threshhold = 0.15
            side_move   = xbox.get_axis(0)
            moveright   = rightkey or side_move > joystick_threshhold
            moveleft    = leftkey or side_move < -joystick_threshhold
            vertical_move = xbox.get_axis(1)
            moveup      = upkey or vertical_move < -joystick_threshhold
            movedown    = downkey or vertical_move > joystick_threshhold

        # handle triggered events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP:
                    moveup, upkey = True, True
                if event.key == K_DOWN:
                    movedown, downkey = True, True
                if event.key == K_RIGHT:
                    moveright, rightkey = True, True
                if event.key == K_LEFT:
                    moveleft, leftkey = True, True
                if event.key == K_SPACE:
                    player.fire()
            elif event.type == KEYUP:
                if event.key == K_UP:
                    moveup, upkey = False, False
                if event.key == K_DOWN:
                    movedown, downkey = False, False
                if event.key == K_RIGHT:
                    moveright, rightkey = False, False
                if event.key == K_LEFT:
                    moveleft, leftkey = False, False
            elif event.type == USEREVENT+1:
                # enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,15))
                # haters.append(enemy)
                difficulty_mult = (level / 3) + 1
                for i in range(0, difficulty_mult):
                    enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,15))
                    haters.append(enemy)


        player.move_up() if moveup else None
        player.move_down() if movedown else None
        player.move_right() if moveright else None
        player.move_left() if moveleft else None
        player.move_mixtapes()

        pre_count = len(haters)
        haters = [h for h in haters if h.x > - _player_height and h.on_fire != 0]
        enemy_count += pre_count - len(haters)
        current_enemy_count += pre_count - len(haters)

        for h in haters:
            h.move()

        hit_count += player.check_hits(haters)

        if player.check_collisions(haters):
            print "Collision"
            break

        if current_enemy_count == enemy_cap:
            current_enemy_count = 0
            # enemy_cap += 3
            level += 1
            player.levelup()
            if enemy_timer > 750:
                enemy_timer -= int(enemy_timer * 0.15)
                pygame.time.set_timer(USEREVENT+1, enemy_timer)


        # prepare screen to be re-drawn
        screen.blit(background, (0, 0))

        # HUD
        # mixtapes remaining
        mixtapes_left = (10,10,10)
        no_mixtapes = (250,0,0)
        text = font.render("Level: {}  Enemies: {}  Hits: {}  Mixtapes: {}"
                .format(level, enemy_count, hit_count, player.mixtapes_remaining), 1,
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

