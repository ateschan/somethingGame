from pygame.locals import *
import pygame
import sys
import math
import os
import subprocess
from random import randint
import engine as e  # this is the engine.py file
clock = pygame.time.Clock()
pygame.init()  # initiates pygame

#CHANGETEXT
# caption shit 
captionlistfilepath = 'titlelist'


def load_captionlist(captionlistfilepath):
    titlelistcount = -1 
    f = open(captionlistfilepath + '.txt')
    data = f.readlines()
    f.close()
    #data = data.split('\n')
    captionlist = []
    for row in data:
        captionlist.append(row)
        titlelistcount += 1
    return (captionlist, titlelistcount)


(captionlist, titlelistcount) = load_captionlist(captionlistfilepath)
pygame.display.set_caption(captionlist[randint(-1, titlelistcount)])


# window caption
WINDOW_SIZEX = 1200
WINDOW_SIZEY = 800
rendx = 390
rendy = 260
displaySize = (rendx, rendy)
jumpercount = 26
killboxcount = 159
screen = pygame.display.set_mode(
    (WINDOW_SIZEX, WINDOW_SIZEY), 0, 32)  # initiate the window

# used as the surface for rendering, which is scaled
display = pygame.Surface((rendx, rendy))


# map load general filepaths
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Loading map, filepaths for animations
e.load_animations('data/images/entities/')
game_map = load_map('map')
grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
jumper_img = pygame.image.load('data/images/jumppad.png')
jumper_ground = pygame.image.load('data/images/jumperground.png')
killbox_image = pygame.image.load('data/images/killbox.png')
main_menu = True
win_menu = False
try_again = False


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()                                                     


class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        font_img = e.swap_color(pygame.image.load(
            path).convert(), (255, 0, 0), (255, 255, 255))
        font_img.set_colorkey((0, 0, 0))
        self.image = font_img
        current_char_width = 0
        self.characters = {}

        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width,
                                0, current_char_width, self.image.get_height())
                self.characters[self.character_order[character_count]
                                ] = char_img.copy()

                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc,):
        x_offset = 0
        for char in text:

            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


my_font = Font('data/images/small_font.png')
my_big_font = Font('data/images/large_font.png')
#Spawn points
player = e.entity(400, 100, 16, 15, 'player', False)
player2 = e.entity(700, 100, 16, 15, 'player2', True)
player_movement = [0,0]
player2_movement = [0,0]

while (main_menu == True):

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is run
            if WINDOW_SIZEX/2 - 90 <= mouse[0] <= WINDOW_SIZEX/2+104 and WINDOW_SIZEY/2 <= mouse[1] <= WINDOW_SIZEY/2+82:
                gameloop = True
                main_menu = False
        if ev.type == pygame.KEYDOWN:
            gameloop = True
            main_menu = False

    # fills the screen with a color
    display.fill((60, 25, 60))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    # if mouse is hovered on a button it
    # changes to lighter shade
    if WINDOW_SIZEX/2 - 90 <= mouse[0] <= WINDOW_SIZEX/2+104 and WINDOW_SIZEY/2 <= mouse[1] <= WINDOW_SIZEY/2+82:
        pygame.draw.rect(display, (70, 35, 70), [
                         rendx/2 - 28, rendy/2 + 7, 63, 20])

    else:
        pygame.draw.rect(display, (50, 15, 50), [
                         rendx/2 - 28, rendy/2 + 7, 62, 20])

    # superimposing the text onto our button
    my_font.render(display, 'Any key to start', (rendx/2 - 150, 60))
    my_big_font.render(display, 'Python Demo', (rendx/2 - 150, 40))
    my_big_font.render(display, 'Start', (rendx/2 - 13, 141))

    # updates the frames of the game
    screen.blit(pygame.transform.scale(
        display, (WINDOW_SIZEX, WINDOW_SIZEY)), (0, 0))

    pygame.display.update()
class jumper_obj():
    def __init__(self, type, loc):
        self.loc = loc
        self.type = type

    def render(self, display, scroll):
        if (self.type == 'pad'):
            display.blit(
                jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
        if (self.type == 'ground'):
            display.blit(
                jumper_ground, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)

    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)
class killbox():
    def __init__(self, type, loc):
        self.loc = loc
        self.type = type

    def render(self, display, scroll):
        if (self.type == 'killbox'):
            display.blit(
                killbox_image, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)

    def collision_test(self, rect):
        killbox_rect = self.get_rect()
        return killbox_rect.colliderect(rect)

# init
jumper_objects = []
P1fireball_list = []
P2fireball_list = []
killbox_objects = []
true_scroll = [0, 0]
P1fireballTimer = 100
P2fireballTimer = 100




# PARALLAX RECTANGLE SHIT
background_objects = [[0.25, [120, 40, 70, 400]], [0.25, [280, 50, 70, 400]], [
    0.5, [30, 70, 40, 400]], [0.5, [130, 120, 100, 400]], [0.5, [300, 110, 120, 400]]]





def render_HUD():
    # HUD
    my_big_font.render(display, (str(player2.score) + " " +
                       str(player.score)), (rendx/2 - 12, 5))
    my_big_font.render(display, (str(P1fireballTimer)), (rendx/2 - 40, 20))
    my_big_font.render(display, (str(P2fireballTimer)), (rendx/2 + 15, 20))

def redrawGameWindow():
    render_HUD()
    screen.blit(pygame.transform.scale(
        display, (WINDOW_SIZEX, WINDOW_SIZEY)), (0, 0))

    pygame.display.update()
    clock.tick(60)

def gamewin(p1, p2):
    win_menu = True
    while (win_menu == True):

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

        # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is run
                if WINDOW_SIZEX/2 - 90 <= mouse[0] <= WINDOW_SIZEX/2+104 and WINDOW_SIZEY/2 <= mouse[1] <= WINDOW_SIZEY/2+82:
                    gameloop = True
                    win_menu = False
                    
            if  ev.type == pygame.KEYDOWN:
                pygame.quit()
                subprocess.call([sys.executable, os.path.realpath('somethingGame.py')] + sys.argv[1:])
                

    # fills the screen with a color
        display.fill((60, 25, 60))

    # stores the (x,y) coordinates into
    # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        # if mouse is hovered on a button it
        # changes to lighter shade
        if WINDOW_SIZEX/2 - 90 <= mouse[0] <= WINDOW_SIZEX/2+104 and WINDOW_SIZEY/2 <= mouse[1] <= WINDOW_SIZEY/2+82:
            pygame.draw.rect(display, (70, 35, 70), [
                rendx/2 - 28, rendy/2 + 7, 58, 20])

        else:
            pygame.draw.rect(display, (50, 15, 50), [
                rendx/2 - 28, rendy/2 + 7, 58, 20])
        if (p1 > p2):

            my_big_font.render(
                display, ' Player 1 WINS! ', (rendx/2 - 150, 50))
        else:
            my_big_font.render(
                display, 'Player 2 WINS! ', (rendx/2 - 150, 50))

        # superimposing the text onto our button
        my_font.render(display, ('by ' + str(abs(p1 - p2)) + " points. Any key to restart"), (rendx/2 - 140, 70))

        my_big_font.render(display, 'Exit', (rendx/2 - 13, 141))
            
        # updates the frames of the game
        screen.blit(pygame.transform.scale(
            display, (WINDOW_SIZEX, WINDOW_SIZEY)), (0, 0))

        pygame.display.update()

while ((gameloop == True) or (try_again == True)):  # GENREAL GAME LOOP
    # winlogic
    if player.score == 3:
        gamewin(player.score, player2.score)
        gameloop = False

    if player2.score == 3:
        gamewin(player.score, player2.score)
        gameloop = False

    display.fill((175, 175, 175))  # clear screen by filling it with gray

    midpointx = (player.x + player2.x)/2
    midpointy = (player.y + player2.y)/2
    zoomx = 0
    zoomy = 0
    # FUCKING ANNOYING CAMERA SCROLLING
    true_scroll[0] += (midpointx - true_scroll[0] - rendx/2)/18
    true_scroll[1] += (midpointy - true_scroll[1] - rendy/2)/18

    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # Temp Horizen Rectangle
    pygame.draw.rect(display, (210, 80, 75), pygame.Rect(0, 120, rendx, rendy))

    # DRAWING THE PARALLAX RACTANGLES
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1]
                               [1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (10, 60, 100), obj_rect)
        else:
            pygame.draw.rect(display, (48, 25, 52), obj_rect)

    # game map rendering the tiles
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '3':
                display.blit(killbox_image, (x*16-scroll[0], y*16-scroll[1]))
                if killboxcount > 0:
                    killbox_objects.append(killbox('killbox', [x*16, y*16]))
                    killboxcount -= 1
            if tile == '4':
                if jumpercount > 0:
                    jumper_objects.append(jumper_obj('pad', [x*16, y*16]))
                    jumpercount -= 1
            if tile == '5':
                if jumpercount > 0:
                    jumper_objects.append(jumper_obj('ground', [x*16, y*16]))
                    jumpercount -= 1

            if tile != '0' and tile != '4' and tile != '5' and tile != '3':
                tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
            x += 1
        y += 1



    # PHYSICS FOR PLAYER 1############################################################################################################
        player_movement[1] = 0
    if player_movement[0] > -.03 and  player_movement[0] < .04:
        player_movement[0] = 0
    else:
        if player_movement[0] > .03:
            player_movement[0] -= .02
        if player_movement[0] < .03:
            player_movement[0] += .02
            
    
    if player.moving_right == True:
        player_movement[0] += .08
    if player.moving_left == True:
        player_movement[0] -= .08
        
        
    player_movement[1] += player.vertical_momentum
    player.vertical_momentum += 0.2
    if player.vertical_momentum > 9:
        player.vertical_momentum = 9

    # PHYSICS FOR PLAYER 2 ############################################################################################################
    player2_movement[1] = 0
    
    if player2_movement[0] > -.03 and player2_movement[0] < .04:
        player2_movement[0] = 0.0
    else:
        if player2_movement[0] > .03:
            player2.set_flip(False)
            player2_movement[0] -= .02
        if player2_movement[0] < .03:
            player2.set_flip(True)
            player2_movement[0] += .02
            
        
    if player2.moving_right == True:
        player2_movement[0] += .08
    if player2.moving_left == True:
        player2_movement[0] -= .08
        
    player2_movement[1] = player2.vertical_momentum
    player2.vertical_momentum += 0.2
    if player2.vertical_momentum > 9:
        player2.vertical_momentum = 9

    fireball_movement = [0, 0]
    for entity in P1fireball_list:
        if (entity.flip == False):
            fireball_movement[0] += 2
        if (entity.flip == True):
            fireball_movement[0] -= 2
        fireball_movement[1] += entity.vertical_momentum
        entity.vertical_momentum += 0.01
        if entity.vertical_momentum > 3:
            entity.vertical_momentum = 1

    p2fireball_movement = [0, 0]
    for entity in P2fireball_list:
        if (entity.flip == False):
            p2fireball_movement[0] += 2
        if (entity.flip == True):
            p2fireball_movement[0] -= 2
        p2fireball_movement[1] += entity.vertical_momentum
        entity.vertical_momentum += 0.01
        if entity.vertical_momentum > 3:
            entity.vertical_momentum = 1

    # JUMPER PADS
    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            player.vertical_momentum = -8

    # JUMPER PADS
    for jumper in jumper_objects:
        if jumper.collision_test(player2.obj.rect):
            player2.vertical_momentum = -8

    # KILLBOXES
    for entity in killbox_objects:
        if entity.collision_test(player.obj.rect):
            player_movement[0] = 0
            player.set_pos(400, 100)
            player.vertical_momentum = 0
            player2.score += 1

        if entity.collision_test(player2.obj.rect):
            player2_movement[0] = 0
            player2.set_pos(400, 100)
            player2.vertical_momentum = 0
            player.score += 1

    # General Player Collision

    if player.collision_test(player2.obj.rect):
        if player.obj.x > player2.obj.x:
            player_movement[0] = 0
            player2_movement[0] = 0
        else:
            player_movement[0] = 0
            player2_movement[0] = 0

        if player.obj.y < player2.obj.y:
            player.vertical_momentum = -2
        if player2.obj.y < player.obj.y:
            player2.vertical_momentum = -2
            
            
            
    
    #Fireball counter cannot be below zero
    if P2fireballTimer < 0:
        P2fireballTimer = 0
    if P1fireballTimer < 0:
        P1fireballTimer = 0
    
    
    #FIREBALL LENGTH
    #Player collision fo the fireball entity
    #now trying to add trail lines to the end of the projectiles
    for entity in P1fireball_list:
        pygame.draw.aaline(display, (255, 50, 50), (player.x - scroll[0] + 5, player.y - scroll[1] + 5), (entity.obj.x - scroll[0] , entity.obj.y - scroll[1] + 5),)
        if player2.collision_test(entity.obj.rect):
            
            player2.tripleJumpCount = 0
            if (entity.flip == True):
                player2_movement[0] -= 2
            else:
                player2_movement[0] += 2
        entity.move(fireball_movement, tile_rects)
        if (entity.obj.block_hit == True):
            P1fireball_list.remove(entity)

    if len(P1fireball_list) > 8:
        for entity in P1fireball_list:
            P1fireball_list.remove(entity)
            P1fireballTimer -= 1


    
    for entity in P2fireball_list:
        pygame.draw.aaline(display, (120, 50, 120), (player2.x - scroll[0] + 5, player2.y - scroll[1] + 5), (entity.obj.x - scroll[0] , entity.obj.y - scroll[1] + 5))
        if player.collision_test(entity.obj.rect):
            player.tripleJumpCount = 0
            if (entity.flip == True):
                player_movement[0] -= 2
            else:
                player_movement[0] += 2
        entity.move(p2fireball_movement, tile_rects)
        if (entity.obj.block_hit == True):
            P2fireball_list.remove(entity)

    if len(P2fireball_list) > 8:
        for entity in P2fireball_list:
            P2fireball_list.remove(entity)
            P2fireballTimer -= 1
    # PLAYER 1 ANIMATION CHECKS########################################################

    if (player_movement[0] == 0) and (player.cancrouch == False) and (player.isjumping == False):
        player.set_action('idle')

    # Crouch check flip animation
    if (player_movement[0] < 0) and (player.isjumping == False) and (player.cancrouch == True):
        player.set_flip(True)
    if (player_movement[0] > 0) and (player.isjumping == False) and (player.cancrouch == True):
        player.set_flip(False)

    # Melee check flip animation

    if (player_movement[0] > 0) and (player.ismelee == True) and (P1fireballTimer != 0):
        P1fireball_list.append(
            e.entity(player.x - 4, player.y - 12, 16, 9, 'fireball', False))

        P1fireballTimer -= 1
        player.set_flip(False)

    if (player_movement[0] < 0) and (player.ismelee == True) and (P1fireballTimer != 0):
        P1fireball_list.append(
            e.entity(player.x - 5, player.y - 12, 16, 9, 'fireball', True))
        P1fireballTimer -= 1
        player.set_flip(True)

    if (player_movement[0] == 0) and (player.ismelee == True) and (player.flip == True) and (P1fireballTimer != 0):
        P1fireball_list.append(
            e.entity(player.x - 5, player.y - 12, 16, 9, 'fireball', True))
        P1fireballTimer -= 1

    if (player_movement[0] == 0) and (player.ismelee == True) and (player.flip == False) and (P1fireballTimer != 0):
        P1fireball_list.append(
            e.entity(player.x - 4, player.y - 12, 16, 9, 'fireball', False))
        P1fireballTimer -= 1

    # if (player.ismelee == False):
    #     for entity in P1fireball_list:
    #          P1fireball_list.remove(entity)

    # Running checck flip animation
    if (player_movement[0] > 0) and (player.isjumping == False) and (player.air_timer == 0) and (player.cancrouch == False):
        player.set_action('run')
        player.set_flip(False)
    if (player_movement[0] < 0) and (player.isjumping == False) and (player.air_timer == 0) and (player.cancrouch == False):
        player.set_action('run')
        player.set_flip(True)

    if (player.tripleJumpCount > 0):
        player.canJumpAgain = True
    else:
        player.canJumpAgain = False
    if (player.canJumpAgain == True):
        player.air_timer = 0

    # PLAYER 2 ANIMATION CHECKS        ########################################################

    if (player2_movement[0] > 0) and (player2.ismelee == True) and (P2fireballTimer != 0):
        P2fireball_list.append(
            e.entity(player2.x - 4, player2.y - 12, 16, 9, 'p2fireball', False))
        P2fireballTimer -= 1
        player2.set_flip(False)

    if (player2_movement[0] < 0) and (player2.ismelee == True) and (P2fireballTimer != 0):
        P2fireball_list.append(
            e.entity(player2.x - 5, player2.y - 12, 16, 9, 'p2fireball', True))
        P2fireballTimer -=1
        player2.set_flip(True)

    if (player2_movement[0] == 0) and (player2.ismelee == True) and (player2.flip == True) and (P2fireballTimer != 0):
        P2fireball_list.append(
            e.entity(player2.x - 5, player2.y - 12, 16, 9, 'p2fireball', True))
        P2fireballTimer -=1

    if (player2_movement[0] == 0) and (player2.ismelee == True) and (player2.flip == False) and (P2fireballTimer != 0):
        P2fireball_list.append(
            e.entity(player2.x - 4, player2.y - 12, 16, 9, 'p2fireball', False))
        P2fireballTimer -=1

    if (player2_movement[0] == 0) and (player2.cancrouch == False):
        player2.set_action('idle')
    if (player2_movement[0] > 0) and (player2.isjumping == False) and (player2.cancrouch == False):
        player2.set_action('run')
        player2.set_flip(False)
    if (player2_movement[0] < 0) and (player2.isjumping == False) and (player2.cancrouch == False):
        player2.set_action('run')
        player2.set_flip(True)
    if (player2_movement[0] < 0) and (player2.cancrouch == True):
        player2.set_flip(True)
    if (player2_movement[0] > 0) and (player2.cancrouch == True):
        player2.set_flip(False)
    if (player2.tripleJumpCount > 0):
        player2.canJumpAgain = True
    else:
        player2.canJumpAgain = False
    if (player2.canJumpAgain == True):
        player2.air_timer = 0

    # COLLISION DETECTION FOR PLAYER 1###############################################
    collision_types = player.move(player_movement, tile_rects)

    if collision_types['right'] == True:
        player.tripleJumpCount = 3
    if collision_types['left'] == True:
        player.tripleJumpCount = 3
    if collision_types['top'] == True:
        player.vertical_momentum = 0
    if collision_types['bottom'] == True:
        player.air_timer = 0
        player.vertical_momentum = 0
        player.tripleJumpCount = 3
    else:
        player.air_timer += 1

    # COLLISION DETECTION FOR PLAYER 2###############################################
    p2collision_types = player2.move(player2_movement, tile_rects)
    if p2collision_types['right'] == True:
        player2.tripleJumpCount = 3
    if p2collision_types['left'] == True:
        player2.tripleJumpCount = 3
    if p2collision_types['top'] == True:
        player2.vertical_momentum = 0
    if p2collision_types['bottom'] == True:
        player2.air_timer = 0
        player2.vertical_momentum = 0
        player2.tripleJumpCount = 3
    else:
        player2.air_timer += 1

    # Animation frame changing per tick
    for entity in P1fireball_list:
        entity.change_frame(1)
        entity.display(display, scroll)


    for entity in P2fireball_list:
        entity.change_frame(1)
        entity.display(display, scroll)


    player2.change_frame(1)
    player.change_frame(1)
    player.display(display, scroll)
    player2.display(display, scroll)

    for event in pygame.event.get():  # event loop

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # MOVEMENT HANDLERS

        # ON KEYPRESS##########################################################################
        if event.type == KEYDOWN:

            # PLAYER 1#############################################
            if event.key == K_g:
                player.ismelee = True
            if event.key == K_s:
                player.obj.y -= 8
                player.cancrouch = True
                player.set_action('crouch')
            if event.key == K_d:
                player.moving_right = True
            if event.key == K_a:
                player.moving_left = True
            if event.key == K_w:
                player.isjumping = True
                if (player.tripleJumpCount > 0):
                    player.tripleJumpCount -= 1
                if player.air_timer < 6:
                    player.vertical_momentum = - 5

            # PLAYER 2#############################################
            if event.key == K_RALT:
                player2.ismelee = True
            if event.key == K_DOWN:
                player2.obj.y -= 8
                player2.cancrouch = True
                player2.set_action('crouch')
            if event.key == K_RIGHT:
                player2.moving_right = True
            if event.key == K_LEFT:
                player2.moving_left = True
            if event.key == K_UP:
                player2.isjumping = True
                if (player2.tripleJumpCount > 0):
                    player2.tripleJumpCount -= 1
                if player2.air_timer < 6:
                    player2.vertical_momentum = - 5

        # ON KEYRELEASE##########################################################################
        if event.type == KEYUP:

            # PLAYER 1#############################################
            if event.key == K_g:
                player.set_action('idle')
                player.ismelee = False
                
            if event.key == K_w:
                player.isjumping = False
            if event.key == K_d:
                player.moving_right = False
            if event.key == K_a:
                player.moving_left = False
            if event.key == K_s:
                if P1fireballTimer < 100:
                    P1fireballTimer += 10
                player.obj.y += 8
                player.cancrouch = False
                player.set_action('crouchgetup')

            # PLAYER 2#############################################
            player2.ismelee = False
                
            if event.key == K_RALT:
                player2.set_action('idle')
                player2.ismelee = False

                
            if event.key == K_LEFT:
                player2.moving_left = False
            if event.key == K_RIGHT:
                player2.moving_right = False
            if event.key == K_DOWN:
                player2.obj.y += 8
                player2.cancrouch = False
                if P2fireballTimer < 100:
                    P2fireballTimer += 10
                player2.set_action('crouchgetup')

    redrawGameWindow()
