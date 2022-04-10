import pygame
import random
import math as m

vec = pygame.math.Vector2



class Ghost:
    def __init__(self, game, pos, number):
        self.game = game
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.number = number
        self.pix_pos = self.get_pix_pos()
        self.colour = self.set_colour()
        self.direction = vec(0,0)
        self.name = self.set_name()
        self.ghost_state = "chase"
        self.target = None
        self.speed = self.set_speed()
        
    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos or self.grid_pos != self.game.player.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        #setting grid position in reference to pixel position
        self.grid_pos[0] = (self.pix_pos[0]-self.game.TOP_BOTTOM_BUFFER + 
                            self.game.CELL_W//2)//self.game.CELL_W+1                              #setting grid position in refernce to pixel position
        self.grid_pos[1] = (self.pix_pos[1]-self.game.TOP_BOTTOM_BUFFER + 
                            self.game.CELL_H//2)//self.game.CELL_H+1

    def draw(self):
        pygame.draw.circle(self.game.display, self.colour,(int(self.pix_pos.x),int(self.pix_pos.y)), self.game.CELL_W//2+2)

    def time_to_move(self):
        if int(self.pix_pos.x+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_W == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True
        if int(self.pix_pos.y+self.game.TOP_BOTTOM_BUFFER//2) % self.game.CELL_H == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True
        return False

    def set_target(self):
        if self.name == "blinky":
            return vec([26,1])
        elif self.name == "pinky":
            return vec([1,1])
        elif self.name == "inky":
            return vec([1,29])
        elif self.name == "clyde":
            return vec([26,29])
        else:
            return vec([15,14])

    def set_speed(self):
        if self.name == "blinky":
            speed = 2
        elif self.name == "pinky":
            speed = 2
        elif self.name == "inky":
            speed = 1
        elif self.name == "clyde":
            speed = 2
        return speed

    def move(self):
        if self.ghost_state == "chase":
            self.colour = self.set_colour()
            if self.name == "blinky":
                self.direction = self.get_path_direction(self.game.player.grid_pos)
            if self.name == "pinky":
                num = random.randint(1,10)
                if num >=6:
                    self.direction = self.get_random_direction(self.direction)
                else:
                    self.direction = self.get_path_direction(self.game.player.grid_pos)
                #xdir = self.game.player.grid_pos[0]+(self.direction.x*4)
                #ydir = self.game.player.grid_pos[1]+(self.direction.y*4)
                #self.direction = self.get_path_direction((vec(xdir, ydir)))
            if self.name == "inky":
                num = random.randint(1,10)
                if num >=8:
                    self.direction = self.get_random_direction(self.direction)
                else:
                    self.direction = self.get_path_direction(self.game.player.grid_pos)
            if self.name == "clyde":
                num = random.randint(1,10)
                if num >=4:
                    self.direction = self.get_random_direction(self.direction)
                else:
                    self.direction = self.get_path_direction(self.game.player.grid_pos)

        if self.ghost_state == "scatter":
            self.direction = self.get_path_direction(self.target)
            

        if self.ghost_state == "frightened":
            self.change_of_state()
            self.colour = (0,0,139)
            self.direction = self.get_random_direction(self.direction)
            
        if self.ghost_state == "eaten":
            self.colour = self.game.WHITE
            self.direction = vec(0,0)


    def get_path_direction(self, target):
        """returns next cell in path to target"""
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target): #target for example = self.game.grid_pos
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [int(target.x), int(target.y)])
        return path[1]

    def BFS(self, start, target):
        """Breadth First Search method"""
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1 #looking through 2d arrays first bracket is y and second is x
        queue = [start]
        path = []
        visited = []
        while queue:  #BFS works on FIFO
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1],[1, 0],[0, 1],[-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1: # means that it is not a wall
                                    queue.append(next_cell)                                
                                    path.append({"Current": current, "Next": next_cell})  #######################Use of dictinoary #####################
                                    
        
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
                    
        return shortest


    def get_random_direction(self, curr_direction):
        """ Method for the random direction when ghosts are frightened"""
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)

            if vec(-x_dir, -y_dir) == curr_direction:
                pass
                
            if next_pos not in self.game.walls:
                break
        return vec(x_dir, y_dir)

    def ghost_eaten(self):
        self.colour = self.game.WHITE
        self.direction = self.get_path_direction([13, 15])
        

    def change_of_state(self):
        self.direction = vec(-self.direction.x, -self.direction.y)

    def blinky(self):
        if self.ghost_state == "chase":
            self.direction = self.get_path_direction(self.game.player.grid_pos)
        elif self.ghost_state == "scatter":
            self.direction = self.get_path_direction([28 , 0])
        elif self.ghost_state == "frightened":
            self.direction = self.get_random_direction(self.direction)
        elif self.ghost_state == "eaten":
            pass


    def inky(self):
        if self.ghost_state == "chase":
            self.direction = self.get_path_direction(self.game.player.grid_pos)
        elif self.ghost_state == "scatter":
            self.direction = self.get_path_direction(28, 30)
        elif self.ghost_state == "frightened":
            self.direction = self.get_random_direction(self.direction)
        elif self.ghost_state == "eaten":
            pass

    def pinky(self):
        if self.ghost_state == "chase":
            xdir = self.game.player.grid_pos[0]+(self.direction.x*4)
            ydir = self.game.player.grid_pos[1]+(self.direction.y*4)
            self.direction = self.get_path_direction(vec(xdir, ydir))
        elif self.ghost_state == "scatter":
            self.direction = self.get_path_direction([0, 0])
        elif self.ghost_state == "frightened":
            self.direction = self.get_random_direction(self.direction)
        elif self.ghost_state == "eaten":
            pass


    def clyde(self):
        if self.ghost_state == "chase":
            self.direction = self.get_path_direction(self.game.player.grid_pos)
        elif self.ghost_state == "scatter":
            self.direction = self.get_path_direction(0, 30)
        elif self.ghost_state == "frightened":
            self.direction = self.get_random_direction(self.direction)
        elif self.ghost_state == "eaten":
            pass


    def frightened(self):
        self.direction = self.get_random_direction()


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
            return "pinky"
        
        if self.number == 1:
            return "inky"

        if self.number == 2:
            return "blinky"

        else:
            return "clyde"