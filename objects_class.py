import pygame
from pygame.math import *
vec = pygame.math.Vector2

class Objects():
    def __init__(self,game):
        self.game = game
        
        

    def super_pellets(self):
        for super_pellets in self.game.super_pellet:
            pygame.draw.circle(self.game.background, self.game.BABY_BLUE, (int(super_pellets.x*self.game.CELL_W)+ self.game.CELL_W//2,
                                                                       int(super_pellets.y*self.game.CELL_H)+self.game.CELL_H//2), 8) 
        

    def pellets(self):
        for pellets in self.game.pellet:
            pygame.draw.circle(self.game.background, self.game.WHITE, (int(pellets.x*self.game.CELL_W)+ self.game.CELL_W//2,
                                                                       int(pellets.y*self.game.CELL_H)+self.game.CELL_H//2), 5) 
        

