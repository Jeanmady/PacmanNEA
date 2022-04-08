import pygame

vec = pygame.math.Vector2



class Ghost:
    def __init__(self, game, pos, number):
        self.game = game
        self.grid_pos = pos
        self.number = number
        self.pix_pos = self.get_pix_pos()
        self.colour = self.set_colour()
        self.direction = vec(0,0)
        self.name = self.set_name()
        
    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move:
            self.move()

    def draw(self):
        pygame.draw.circle(self.game.display, self.colour,(int(self.pix_pos.x),int(self.pix_pos.y)), self.game.CELL_W//2+2)

    def time_to_move(self):
        pass

    def move(self):
        pass

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.game.CELL_W)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_W // 2,
                            (self.grid_pos.y*self.game.CELL_H)+self.game.TOP_BOTTOM_BUFFER//2 + self.game.CELL_H // 2)

    def set_colour(self):
        if self.number == 0:
            return (234,130,229)

        if self.number == 1:
            return (70,191,238)

        if self.number == 2:
            return (208,62,25)

        if self.number == 3:
            return (219,133,28)

    def set_name(self):
        if self.number == 0:
            return "Pinky"
        
        if self.number == 1:
            return "Inky"

        if self.number == 2:
            return "Blinky"

        else:
            return "Clyde"