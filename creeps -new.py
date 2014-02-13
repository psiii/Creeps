#import creeps
from creeplib import *
import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite

from vec2d import vec2d

def run_game():
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280,1024
    BG_COLOR = 150, 150, 80
    N_EATERS = 10
    N_BALANCERS = 30
    N_VICTIMS =50
    creeps = list()
    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    
    # Create N_CREEPS random creeps.
    def appendEater():
        creeps.append(Eater(screen,    (   randint(0, SCREEN_WIDTH),
                                randint(0, SCREEN_HEIGHT)),
                            (   choice([-1, 1]),
                                choice([-1, 1])),
                            0.05))

    def appendBalancer():
        creeps.append(Balancer(screen,    (   randint(0, SCREEN_WIDTH),
                                randint(0, SCREEN_HEIGHT)),
                            (   choice([-1, 1]),
                                choice([-1, 1])),
                            0.1))
    def appendVictim():
        creeps.append(Victim(screen,    (   randint(0, SCREEN_WIDTH),
                                randint(0, SCREEN_HEIGHT)),
                            (   choice([-1, 1]),
                                choice([-1, 1])),
                            0.2))

    for i in range(N_EATERS):
        appendEater()
    for i in range(N_BALANCERS):
        appendBalancer()
    for i in range(N_VICTIMS):
        appendVictim()
        
    keyspressed=0
    # The main game loop
    c=0
    VMAX=0
    while True:
        # Limit frame speed to 50 FPS
        #
        time_passed = clock.tick(50)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        # Redraw the background
        screen.fill(BG_COLOR)
        
        # Update and redraw all creeps
        foodlist = []
        VCOUNT = 0
        ECOUNT = 0
        for creep in creeps:
            creep.update(time_passed)
            creep.blitme()
            if not creep.isdead():
                foodlist.append(creep)
                if creep.getspecies()==0:
                    VCOUNT+=1
                elif creep.getspecies()==2:
                    ECOUNT+=1
            elif creep.isdead():
                creeps.remove(creep)
        if VCOUNT>VMAX:
            VMAX=VCOUNT
        print 'Current victims:',VCOUNT,' Max seen:', VMAX
        for creep1 in foodlist:
            foodlist.remove(creep1)
            for creep2 in foodlist:
                
                if creep1.getposition().colliderect(creep2.getposition()):
                    if (creep1.getspecies() == creep2.getspecies()):
                        if (creep2.getcooldown()==0 and
                            (creep1.gethunger()==0 and creep2.gethunger==0)):
                            creep2.invdirection()
                            creep2.reprod()
                            creep1.reprod()
                            if creep1.getspecies() is 0 and VCOUNT>150:
                                print ''
                            elif creep2.getspecies() is 2 and ECOUNT>30:
                                print ''
                            else:
                                appendVictim()
                    elif creep1.getspecies() == (creep2.getspecies()+1):
                        creep1.eat()                    
                        creep2.die()                    
                    elif creep1.getspecies() == (creep2.getspecies()-1):
                        creep2.eat()
                        creep1.die()

        pygame.display.flip()

def exit_game():
    sys.exit()
run_game()

