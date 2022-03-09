import pygame
from menu import MainMenu


class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.DISPLAY_W = 480*2
        self.DISPLAY_H = 270*2
        self.display = pygame.display.set_mode((self.DISPLAY_H, self.DISPLAY_W))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        #self.font_name = pygame.font.get_default_font()    #vhange later
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        #self.main_menu = MainMenu(self)  #refrence main menu object
        self.curr_menu = MainMenu(self)   #enables current menu to be chanegd depenfin gon whats selected
        
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:   #enter key to pause and unpause
                self.playing = True
            self.display.fill(self.BLACK) # gets rid of images by ressting screen
            self.draw_text('THis is where the game will be ', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0)) #
            pygame.display.update() # moves image onto screen
            self.reset_keys()

            
    def check_events(self):    #Checks whenever user enters a key 
        for event in pygame.event.get():  #goes through a list of everything player can do on computer
            if event.type == pygame.QUIT:  #checks if user closes window
                 self.running, self.playing = False, False
                 self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:  #checks if user presses something on keyboard
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    
    def reset_keys(self):  #function to reset keys
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False

    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE) #creates a rectangular image of text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        
