import pygame
from pygame.math import *
vec = pygame.math.Vector2
from databse import *
from Current_score import *
import time


class Player:
    def __init__(self, game, pos):
        self.PLAYER_C = (253,255,0)
        self.RED = (252, 3, 3)
        self.game = game
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        #print(self.grid_pos, self.pix_pos)
        self.direction = vec(1,0)
        self.speed = 2
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.DatabaseActions = DatabaseActions(self)
        self.lifes = 3
        self.speed_timer = 0
        self.scared_timer = 0

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.game.CELL_W)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_W // 2,
                            (self.grid_pos[1]*self.game.CELL_H)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_H // 2)
        

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
                if self.stored_direction != None:
                    self.direction = self.stored_direction
                self.able_to_move = self.can_move()
                
        self.grid_pos[0] = (self.pix_pos[0]-self.game.TOP_BOTTOM_BUFFER + 
                            self.game.CELL_W//2)//self.game.CELL_W+1                              #setting grid position in refernce to pixel position
        self.grid_pos[1] = (self.pix_pos[1]-self.game.TOP_BOTTOM_BUFFER + 
                            self.game.CELL_H//2)//self.game.CELL_H+1

        if self.on_pellet(self.game.pellet):
            self.eat_pellet(self.game.pellet)

        elif self.on_super_pellet(self.game.super_pellet):
            self.eat_super_pellet(self.game.super_pellet)
            self.game.ghost_state("frightened")
            self.scared_timer = 1300

        if self.on_extra_life(self.game.extra_life):
            self.eat_extra_life(self.game.extra_life)
            self.lifes += 1

        if self.on_speed_fruit(self.game.speed_fruit):
            self.eat_speed_fruit(self.game.speed_fruit)
            self.speed = 4
            self.speed_timer = 8

        self.speed_timer -= 1
        if self.speed_timer <= 0:
            self.speed = 2

        self.scared_timer -=1
        if self.scared_timer <= 0:
            self.game.ghost_state("chase")
        
        self.DatabaseActions.update_score(int(self.current_score))
        if self.current_score > int(self.DatabaseActions.get_current_highscore()):
            self.DatabaseActions.update_current_highscore(self.current_score)
    
    def draw(self):
        pygame.draw.circle(self.game.display, self.PLAYER_C, (int(self.pix_pos.x), int(self.pix_pos.y)), self.game.CELL_W//2+2)
        #draws the rectangle for the position of player
        """pygame.draw.rect(self.game.display, self.RED, (self.grid_pos[0] * self.game.CELL_W+self.game.TOP_BOTTOM_BUFFER//2, 
                                                        self.grid_pos[1] * self.game.CELL_H+self.game.TOP_BOTTOM_BUFFER//2, 
                                                        self.game.CELL_W, self.game.CELL_H), 1) """
        #drawing player lifes
        for x in range(self.lifes):
            pygame.draw.circle(self.game.display, self.RED, (30 + 20*x, 655), 8)

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self):
        if int(self.pix_pos.x+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_W == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):#forgot to allow her efor no movement                
                return True
        if int(self.pix_pos.y+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_H == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True
       
    def can_move(self):
        for wall in self.game.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

       
    def on_pellet(self, item):
        if self.grid_pos in item:
            return True
        return False
            
    def eat_pellet(self, item):
        item.remove(self.grid_pos)
        self.current_score += 10

    def on_super_pellet(self, item):
        if self.grid_pos in item:
            return True
        return False       

    def eat_super_pellet(self, item):
        item.remove(self.grid_pos)
        self.current_score += 50


    def on_speed_fruit(self, item):
        if self.grid_pos in item:
            return True
        return False
    
    def eat_speed_fruit(self, item):
        item.remove(self.grid_pos)

    def on_extra_life(self, item):
        if self.grid_pos in item:
            return True
        return False
    
    def eat_extra_life(self, item):
        item.remove(self.grid_pos)


    
    def super_pellets(self):
        for super_pellets in self.game.super_pellet:
            pygame.draw.circle(self.game.display, self.game.BABY_BLUE, (int(super_pellets.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(super_pellets.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 5) 
        

    def pellets(self):
        for pellets in self.game.pellet:
            pygame.draw.circle(self.game.display, self.game.WHITE, (int(pellets.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(pellets.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 3)
    
    def speed_fruit(self):
        for speed_fruits in self.game.speed_fruit:
            pygame.draw.circle(self.game.display, self.game.GREEN, (int(speed_fruits.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(speed_fruits.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 6)

    def extra_life(self):
        for extra_lifes in self.game.extra_life:
            pygame.draw.circle(self.game.display, self.RED, (int(extra_lifes.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(extra_lifes.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 6) 
        

        
    