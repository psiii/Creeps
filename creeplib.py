from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite

from vec2d import vec2d

class Creep(Sprite):

    def __init__(   
            self, screen, img_filename, init_position, 
            init_direction, speed, species, agelimit):
        Sprite.__init__(self)
        self.state = 1
        self.species = species
        self.screen = screen
        self.speed = speed
        self.base_image = pygame.image.load(img_filename).convert_alpha()
        self.image = self.base_image
        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.cooldown = 0
        self.age=0
        self.agelimit=agelimit
        self.hunger=1
        
    def update(self, time_passed):
        self.age+=time_passed
        if self.age > self.agelimit:
            self.die()
        self._change_direction(time_passed)
        self.image = pygame.transform.rotate(
            self.base_image, -self.direction.angle)
        
        displacement = vec2d(    
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)
        
        self.pos += displacement
        
        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(
                        -self.image_w, -self.image_h)
        
        if self.pos.x < bounds_rect.left:
            self.pos.x = bounds_rect.left
            self.direction.x *= -1
        elif self.pos.x > bounds_rect.right:
            self.pos.x = bounds_rect.right
            self.direction.x *= -1
        elif self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom
            self.direction.y *= -1
    
    def blitme(self):
        draw_pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_pos)

    def getspecies(self):
        return self.species
    
    def getposition(self):
        pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2)
        return pos

    def getcooldown(self):
        return self.cooldown

    def getdirection(self):
        return self.direction

    def setdirection(self, direction):
        self.direction = vec2d(direction).normalized()
        
    def gethunger(self):
        return self.hunger
    
    def eat(self):
        self.hunger=0
        self.age=self.age
        print 'a'
        
    def reprod(self):
        self.speed=self.speed
        self.hunger=1
        
    def invdirection(self):
        x=randint(0,1)
        if x == 0:
            self.direction.x *= -1
        elif x == 1:
            self.direction.y *= -1
        self.cooldown = 1000
        return self.cooldown
            
    def setspeed(self,speed):
        self.speed=speed

    def die(self):
        self.state=0

    def isdead(self):
        if self.state==0:
            return True
        else:
            return False
       
    #------------------ PRIVATE PARTS ------------------#
    _counter = 0
    def _change_direction(self, time_passed):
        self._counter += time_passed 
        if self.cooldown > 0:
            self.cooldown -= time_passed
        elif self.cooldown <0:
            self.cooldown = 0
        if self._counter > randint(1000, 1500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0



class Eater(Creep):
    def __init__(self, screen, init_position,init_direction, speed):
        Creep.__init__(self, screen, 'pinkcreep.png', init_position,init_direction, speed, 2, 60000)

    def eat(self):
        self.age=0
        self.hunger=0
       # print 'b'

class Balancer(Creep):
    def __init__(self, screen, init_position,init_direction, speed):
        Creep.__init__(self, screen, 'bluecreep.png', init_position,init_direction, speed, 1, 10000)
    
    def eat(self):
        self.age=self.age-1000
        if self.age<0:
            self.age=0
        self.hunger=0
        
        
class Victim(Creep):
    def __init__(self, screen, init_position,init_direction, speed):
        Creep.__init__(self, screen, 'graycreep.png', init_position,init_direction, speed, 0, 10000)
        self.hunger=0
    
    def reprod(self):
        self.hunger=0
        print 'asd'

