import pygame
from pygame.math import Vector2 as vec
import copy
from menu import *
from player import *
from databse import *
from ghosts import *


class Game():
    """ Attributes """
    def __init__(self):
        pygame.init()
        self.login = True
        self.running = True #state boolean variables
        #boolean variables for user input
        self.mainstate = 'startup'
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.UNICODE_KEY = False, False, False, False, False, False, False 
        self.TOP_BOTTOM_BUFFER = 50
        self.FPS = 60
        self.UNICODE_KEY = False
        self.DISPLAY_W = 480*1.5
        self.DISPLAY_H = 270*1.5 
        self.MAZE_W = 560
        self.MAZE_H = 620
        self.CELL_W = self.MAZE_W // 28
        self.CELL_H = self.MAZE_H // 30
        self.unicode_text = ''
        self.display = pygame.display.set_mode((self.DISPLAY_H, self.DISPLAY_W))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name_defult = pygame.font.Font(None, 20)   
        self.font_name_8bit = '8-BIT WONDER.TTF'
        self.font_name_pacmanio = 'PacmanioFont.TTF'
        self.BLACK, self.WHITE, self.GREY, self.BABY_BLUE, self.GREEN, self.RED = (0,0,0), (255,255,255), (107,107,107), (137,207,240), (0,255,0), (252, 3, 3)
        self.main_menu = MainMenu(self)     #refrence main menu object
        self.add_friends_menu = AddFriends(self)
        self.controls_menu = GameControls(self)
        self.register_menu = RegisterMenu(self)
        self.startup_menu = StartUpMenu(self)         #enables current menu to be chanegd depenfin gon whats selected
        self.signin_menu = SignInMenu(self)
        self.boards_menu = ScoreBoards(self)
        self.DatabaseActions = DatabaseActions(self)
        self.gameover_menu = GameOver(self)
        self.clock = pygame.time.Clock()
        self.walls, self.pellet, self.super_pellet ,self.speed_fruit, self.extra_life = [], [], [], [], []
        self.ghosts = []
        self.GHOST_POS, self.PLAYER_START = [], None
        self.load()
        self.player = Player(self, vec(self.PLAYER_START))
        self.make_ghosts()
        

    """ Methods """
    def game_loop(self): # This runs the whole program checking th e main state to see what is running and chabges it when the mainstate changes
        while self.running:
            if self.mainstate == 'startup':
            
                self.startup_menu.display_menu()

            elif self.mainstate == 'register':
                self.register_menu.display_menu()

            elif self.mainstate == 'login':
                self.signin_menu.display_menu()

            elif self.mainstate == 'mainmenu':
                self.main_menu.display_menu()

            elif self.mainstate == 'controls':
                self.controls_menu.display_menu()

            elif self.mainstate == 'addfriends':
                self.add_friends_menu.display_menu()

            elif self.mainstate == 'boards':
                self.boards_menu.display_menu()

            elif self.mainstate == 'playing':
                self.display = pygame.display.set_mode((610, 670))
                self.current_highscore = self.DatabaseActions.get_current_highscore()
                self.playing_events()
                self.playing_updates()
                self.playing_draw()

            elif self.mainstate == 'gameover':
                self.display = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
                self.current_highscore = self.DatabaseActions.get_current_highscore()
                self.gameover_menu.display_menu()
                
            else:
                self.running = False
            self.clock.tick(self.FPS)

################################# MULTIUSE HELPER FUNCTIONS #################################

    def get_highscores_dict(self, table):
        value_key_pairs = ((value, key) for (key,value) in table.items())
        sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
        global_board = {k: v for v, k in sorted_value_key_pairs}
        return global_board

    def draw_grid(self):
        for x in range(self.MAZE_W//self.CELL_W):
            pygame.draw.line(self.background, self.GREY, (x*self.CELL_W, 0), (x*self.CELL_W, self.MAZE_H))
        for x in range(self.MAZE_H//self.CELL_H):
            pygame.draw.line(self.background, self.GREY, (0, x*self.CELL_H), ( self.MAZE_W,x*self.CELL_H))
        for wall in self.walls:
            pygame.draw.rect(self.background, (112, 55, 163), (wall.x*self.CELL_W, wall.y*self.CELL_H, self.CELL_H, self.CELL_H))

    def load(self): # loads backgrounds
        self.background = pygame.image.load('backgroundMaze.png')
        self.background = pygame.transform.scale(self.background, (self.MAZE_W, self.MAZE_H))

        with open("walls.txt", 'r') as file:   #openeing walls file
            for yidx, line in enumerate(file):   # creating the walls list using coords of the walls in txt file
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))  # then it srtores it as a vector
                    elif char == "P":
                        self.pellet.append(vec(xidx, yidx)) # here lin to function where we can randomly assign tiems to that spot
                    elif char == "S":
                        self.super_pellet.append(vec(xidx, yidx))
                    elif char == "U":
                        self.PLAYER_START = [xidx, yidx]
                    elif char in ["2","3","4","5"]:
                        self.GHOST_POS.append(vec(xidx, yidx))
                    elif char == "R":
                        self.random_object().append(vec(xidx, yidx))
                   
    def random_object(self):
        chance = random.randint(1,10)
        if chance <= 6:
            return self.speed_fruit
        else:
            return self.extra_life
                    

    def make_ghosts(self):
        for idx, pos in enumerate(self.GHOST_POS):
            self.ghosts.append(Ghost(self, vec(pos), idx))

    def reset(self):
        self.player.lifes = 3
        self.player.current_score = 0
        

        self.pellet = []
        self.super_pellet = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'P':
                        self.pellet.append(vec(xidx, yidx))
                    elif char == 'S':
                        self.super_pellet.append(vec(xidx, yidx))
                    elif char == 'R':
                        self.random_object().append(vec(xidx, yidx))
        self.mainstate = "playing"
        
                    

    def draw_text_8bit(self, text, size, x,y):   #try add left organisatoion in order to block fonts later down the line   16/03/22
        """ Method to draw text using 8bit font """
        font = pygame.font.Font(self.font_name_8bit,size)
        text_surface = font.render(text, True, self.WHITE) #creates a rectangular image of text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_text_Pacmanio(self, text, size, x,y):   #try add left organisatoion in order to block fonts later down the line   16/03/22
        """ Method to draw text using 8bit font """
        font = pygame.font.Font(self.font_name_pacmanio,size)
        text_surface = font.render(text, True, self.WHITE) #creates a rectangular image of text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_text(self, text, size, x,y):
        """ Method to draw text using regular font """
        font =  self.font_name_defult
        text_surface = font.render(text, True, self.WHITE) #creates a rectangular image of text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_text_bottom_left(self, text, size, x,y):
        """ Method to create text using bottom left as organiser """
        font = self.font_name_defult
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_text_bottom_right(self, text, size, x,y):
        """ Method to create text using bottom right as organiser """
        font = self.font_name_defult
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midright = (x,y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):  
        """ Method to reset keys """
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.LEFT_KEY = False
        self.RIGHT_KEY = False
        self.UNICODE_KEY = False
    
    def check_events(self):
        """ Method to check whenever user enters a key """
        for event in pygame.event.get():      #goes through a list of everything player can do on computer
            if event.type == pygame.QUIT:       #checks if user closes window
                self.running = False
            if event.type == pygame.KEYDOWN:          #checks if user presses something on keyboard
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                else:
                    self.UNICODE_KEY = True
                    self.unicode_text = event.unicode    



################################# PLAYING FUNCTIONS #################################

    def playing_events(self):
            for event in pygame.event.get():                                                                        #goes through a list of everything player can do on computer
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:                                                                    #checks if user presses something on keyboard
                    if event.key == pygame.K_DOWN:
                        self.player.move(vec(0,1))
                    if event.key == pygame.K_UP:
                        self.player.move(vec(0,-1))
                    if event.key == pygame.K_LEFT:
                        self.player.move(vec(-1,0))
                    if event.key == pygame.K_RIGHT:
                        self.player.move(vec(1,0))

    def playing_updates(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()

        for ghost in self.ghosts:
            if ghost.grid_pos == self.player.grid_pos:
                if ghost.ghost_state =="chase":
                    self.remove_life()
                elif ghost.ghost_state == "frightened":
                    ghost.ghost_state = "eaten"
                    self.player.current_score += 200

    def ghost_state(self, state):
        for ghost in self.ghosts:
            ghost.ghost_state = state

    def playing_draw(self):
        self.display.fill(self.BLACK)
        self.display.blit(self.background, (self.TOP_BOTTOM_BUFFER//2, self.TOP_BOTTOM_BUFFER//2))      
        self.player.pellets()
        self.player.super_pellets()
        self.player.speed_fruit()
        self.player.extra_life()
        self.draw_text_bottom_left(('HIGHSCORE: {}'.format(self.DatabaseActions.get_current_highscore())), 16, 5, 10)
        self.draw_text_bottom_right(('SCORE: {}'.format(self.DatabaseActions.get_current_score())), 16, 595, 10)      
        #self.draw_grid() # add writing and text in here ~~~~~~ REMOVE HASHTAG TO DRAW GRID
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.playing_updates()    
        pygame.display.update()

    def remove_life(self):
        self.player.lifes -= 1
        if self.player.lifes == 0:
            self.DatabaseActions.update_highscore(int(self.DatabaseActions.get_current_userid()), int(self.DatabaseActions.get_current_highscore()))
            self.mainstate = "gameover"

        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *=0
            for ghost in self.ghosts:
                ghost.grid_pos = vec(ghost.starting_pos)
                ghost.pix_pos = ghost.get_pix_pos()
                ghost.direction *= 0

                

        
