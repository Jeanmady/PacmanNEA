import pygame
from pygame.math import *
vec = pygame.math.Vector2
class Player:
    def __init__(self, game, pos):
        self.PLAYER_C = (190,194,15)
        self.RED = (252, 3, 3)
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x*self.game.CELL_W + self.game.CELL_W // 2,
        self.grid_pos.y*self.game.CELL_H + self.game.CELL_H // 2)
        print(self.grid_pos, self.pix_pos)
        self.direction = vec(1,0)

    def update(self):
        self.pix_pos += self.direction
        self.grid_pos[0] = (self.pix_pos[0]+self.game.CELL_W//2)//(self.game.CELL_W+1)  #setting grid position in refernce to pixel position
        self.grid_pos[1] = (self.pix_pos[1]+self.game.CELL_H//2)//(self.game.CELL_H+1)
    
    def draw(self):
        pygame.draw.circle(self.game.display, self.PLAYER_C, ((int(self.pix_pos.x), int(self.pix_pos.y))), self.game.CELL_W//2-1)
        #draws the rectangle for the position of player
        pygame.draw.rect(self.game.display, self.RED, (self.grid_pos[0] * self.game.CELL_W, self.grid_pos[1] * self.game.CELL_H, self.game.CELL_W, self.game.CELL_H), 1) 

    def move(self, direction):
        self.direction = direction
       
    