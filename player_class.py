import pygame
from pygame.math import *
vec = pygame.math.Vector2
class Player:
    def __init__(self, game, pos):
        self.PLAYER_C = (190,194,15)
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x*self.game.CELL_W,
        self.grid_pos.y*self.game.CELL_H)
        print(self.grid_pos, self.pix_pos)
    
    def draw(self):
        pygame.draw.circle(self.game.display, self.PLAYER_C, (int(self.pix_pos.x), int(self.pix_pos.y)), self.game.CELL_W//2-2)
       