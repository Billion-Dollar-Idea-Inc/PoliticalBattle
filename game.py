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

    def __init__(self, x, y, height, speed_diff):
        pygame.sprite.Sprite.__init__(self)

        enemy_options = [
            'hater.png',
            'hater_1.png',
            'hater_2.png',
            'hater_3.png',
            'hater_4.png'
        ]
        pick = random.randrange(0, len(enemy_options))

        # info about image
        self.image, self.rect = load_png(enemy_options[pick])
        self.fire, self.fire_rect = load_png('fire.png')
        self.height = self.rect.height
        self.width = self.rect.width
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.on_fire = -1
        self.move_dist = int(height * 0.014) + speed_diff
        if self.move_dist is 0:
            self.move_dist = int(height * 0.014)

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

    def __init__(self, x, y, height):
        pygame.sprite.Sprite.__init__(self)

        # info about image
        self.image, self.rect = load_png('tmp_user_art.png')
        #self.image, self.rect = load_png('mixtape.png')
        self.rect.left = x
        self.rect.top = y
        self.height = self.rect.height
        self.width = self.rect.width
        self.consumed = False
        self.move_dist = int(height * 0.022)

    def move(self):
        self.rect.left += self.move_dist

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class player_obj(pygame.sprite.Sprite):

    def __init__(self, x, y, level=1):
        pygame.sprite.Sprite.__init__(self)

        # info about image
        self.image, self.rect = load_png('player.png')
        self.height = self.rect.height
        self.width = self.rect.width
        self.x = x
        self.y = (y - self.height) / 2
        self.max_y = y
        self.rect.left = x
        self.rect.top = (y - self.height) / 2
        self.move_dist = int(y * 0.012)

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
            fire_sounds = ['boom.wav', 'bop.wav', 'bada.wav', 'pow.wav']
            self.fire_sound = [pygame.mixer.Sound(load_wav(s)) for s in fire_sounds]
            # self.fire_sound = pygame.mixer.Sound(load_wav('superhot.wav'))
            self.empty_sound = pygame.mixer.Sound(load_wav('EmptyClip.wav'))
            self.not_rapper_sound = pygame.mixer.Sound(load_wav('ImNotARapper.wav'))

    def levelup(self):
        self.level += 1
        self.mixtapes_remaining += 4 + (self.level * 2)

    def get_rect(self):
        return self.rect

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
        surface.blit(self.image, self.rect)
        for tape in self.mixtapes:
            tape.draw(surface)

    def fire(self):
        if self.mixtapes_remaining > 0:
            b = mixtape_obj(self.x + self.width, self.y + self.height/3, self.max_y)
            self.mixtapes.append(b)
            self.mixtapes_remaining -= 1
            if _audio_enabled:
                #self.fire_sound.stop() #Stop previous sound if there was one
                self.fire_sound[random.randrange(0,len(self.fire_sound))].play(loops=0, maxtime=0)
                # self.fire_sound.play(loops=0, maxtime=0) # "supa hot"
        else:
            if _audio_enabled:
                self.empty_sound.play(loops=0, maxtime=0) # "supa hot"


    def taunt(self):
        if _audio_enabled:
            self.not_rapper_sound.play(loops=0, maxtime=0) # "supa hot"

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
    _audio_enabled = False if '--disable-audio' in sys.argv else True

    # pre_init Pygame audio mixer
    if _audio_enabled:
        pygame.mixer.pre_init(frequency=22050, buffer=(2**20))

    pygame.init()
    if _audio_enabled:
        pygame.mixer.init()
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

    #Background music
    if _audio_enabled:
        pygame.mixer.music.load(os.path.join('data', 'rickrosslow.ogg'))
        pygame.mixer.music.play(-1)
        lose_sound = pygame.mixer.Sound(load_wav('stop.wav'))
        level_sound = pygame.mixer.Sound(load_wav('superhot.wav'))

    # Initialise screen
    pygame.display.set_caption('StraightFire')
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, 0)
    # screen = pygame.display.set_mode((0,0))
    (_width, _height) = screen.get_size()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # background.fill((250, 250, 250))
    background = pygame.image.load("data/darktown.png").convert()

    # Initialize player
    player = player_obj(0, _height, 1)
    player_info = player.get_rect()
    _player_width, _player_height = player_info[2], player_info[3]
    # return

    # Initialize sprites
    playersprite = pygame.sprite.RenderPlain((player))

    # Initialize text
    font = pygame.font.Font(None, 32)
    mixtape_font = pygame.font.Font(None, 48)
    title_font = pygame.font.Font(None, 162)

    # Blit everything to the screen
    screen.blit(background, (-500, -500))
    #screen.blit(bg, (0, 0))
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
    wave_mult = 1

    # controller vars
    enable_360 = False
    fire_enabled = True
    taunt_enabled = True

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if len(joysticks) > 0:
        xbox = joysticks[0]
        xbox.init()
        enable_360=True


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
                enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,30),
                        _height, random.randrange(-level, level))
                haters.append(enemy)
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
                if event.key == K_t:
                    player.taunt()
                    enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,30),
                        _height, random.randrange(-level, level))
                    haters.append(enemy)
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
                wave_mult = (level / 3) + 1
                for i in range(0, wave_mult):
                    enemy = enemy_obj(_width, random.randrange(0,_height-_player_height,30),
                        _height, random.randrange(-level, level))
                    haters.append(enemy)

        # do movement
        player.move_up() if moveup else None
        player.move_down() if movedown else None
        player.move_right() if moveright else None
        player.move_left() if moveleft else None
        player.move_mixtapes()

        pre_count = len(haters)
        haters = [h for h in haters if h.x > -_player_width and h.on_fire != 0]
        enemy_count += pre_count - len(haters)
        current_enemy_count += pre_count - len(haters)

        for h in haters:
            h.move()

        hit_count += player.check_hits(haters)

        if player.check_collisions(haters):
            break

        # scale difficulty
        if current_enemy_count >= wave_mult * enemy_cap:
            current_enemy_count = 0
            enemy_cap += 1
            level += 1
            player.levelup()
            if enemy_timer > 750:
                enemy_timer -= int(enemy_timer * 0.15)
                pygame.time.set_timer(USEREVENT+1, enemy_timer)
            # show levelup screen
            text = title_font.render("Level {}".format(level),1,(250,250,250))
            textpos = text.get_rect()
            textpos.centerx = _width / 2
            textpos.centery = _height/ 2 - 75
            screen.blit(text, textpos)
            if _audio_enabled:
                level_sound.play(loops=0, maxtime=0)
            pygame.display.flip()
            pygame.time.wait(1500)
            text2 = title_font.render("Go!".format(level),1,(250,250,250))
            textpos2 = text2.get_rect()
            textpos2.centerx = _width / 2
            textpos2.centery = _height/ 2 + 75
            screen.blit(text, textpos)
            screen.blit(text2, textpos2)
            pygame.display.flip()
            pygame.time.wait(1000)


        # prepare screen to be re-drawn
        screen.blit(background, (-500, -500))
        # screen.blit(background, (0,0))

        # HUD
        # mixtapes remaining
        mixtapes_left = (250,250,250)
        no_mixtapes = (250,0,0)
        mixtape_text = mixtape_font.render("Mixtapes: {}".format(player.mixtapes_remaining),
            1, mixtapes_left if player.mixtapes_remaining > 0 else no_mixtapes)
        mixtape_pos = mixtape_text.get_rect()
        mixtape_pos.x = 15
        mixtape_pos.y = 15
        screen.blit(mixtape_text, mixtape_pos)
            
        text = font.render("Level: {}   Haters: {}   Hits: {}"
                .format(level, enemy_count, hit_count), 1, mixtapes_left)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx - 500
        textpos.centery = 15
        screen.blit(text, textpos)

        # playersprite.update()
        player.draw(screen)
        for h in haters:
            h.draw(screen)
        pygame.display.flip()

    text = title_font.render("Your mixtape flopped!", 1, (255,20,0))
    textpos = text.get_rect()
    textpos.centerx = _width / 2
    textpos.centery = _height/ 2
    screen.blit(text, textpos)
    pygame.display.flip()
    if _audio_enabled:
        lose_sound.play(loops=0, maxtime=0)
    pygame.time.wait(2000)
    
if __name__ == '__main__': main()

