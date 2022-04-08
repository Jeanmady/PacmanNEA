import pygame
from pygame.math import *
vec = pygame.math.Vector2
from databse import *
from Current_score import *

class Player:
    def __init__(self, game, pos):
        self.PLAYER_C = (190,194,15)
        self.RED = (252, 3, 3)
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vec((self.grid_pos.x*self.game.CELL_W)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_W // 2,
                            (self.grid_pos.y*self.game.CELL_H)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_H // 2)
        #print(self.grid_pos, self.pix_pos)
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.DatabaseActions = DatabaseActions(self)

        

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction
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


        self.DatabaseActions.update_score(int(self.current_score))
    
    def draw(self):
        pygame.draw.circle(self.game.display, self.PLAYER_C, (int(self.pix_pos.x), int(self.pix_pos.y)), self.game.CELL_W//2+2)
        #draws the rectangle for the position of player
        """pygame.draw.rect(self.game.display, self.RED, (self.grid_pos[0] * self.game.CELL_W+self.game.TOP_BOTTOM_BUFFER//2, 
                                                        self.grid_pos[1] * self.game.CELL_H+self.game.TOP_BOTTOM_BUFFER//2, 
                                                        self.game.CELL_W, self.game.CELL_H), 1) """

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self):
        if int(self.pix_pos.x+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_W == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pix_pos.y+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_H == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
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

    def grace_fruit(self):
        pass

    def freeze_fruit(self):
        pass

    def super_pellets(self):
        for super_pellets in self.game.super_pellet:
            pygame.draw.circle(self.game.display, self.game.BABY_BLUE, (int(super_pellets.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(super_pellets.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 5) 
        

    def pellets(self):
        for pellets in self.game.pellet:
            pygame.draw.circle(self.game.display, self.game.WHITE, (int(pellets.x*self.game.CELL_W)+ self.game.CELL_W//2+self.game.TOP_BOTTOM_BUFFER//2,
                                                                       int(pellets.y*self.game.CELL_H)+self.game.CELL_H//2+self.game.TOP_BOTTOM_BUFFER//2), 3) 
        

        
    