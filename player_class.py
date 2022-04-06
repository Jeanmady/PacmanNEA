import pygame
from pygame.math import *
vec = pygame.math.Vector2
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
    
    def draw(self):
        pygame.draw.circle(self.game.display, self.PLAYER_C, (int(self.pix_pos.x), int(self.pix_pos.y)), self.game.CELL_W//2-2)
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

        
    