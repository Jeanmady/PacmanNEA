import pygame

class Game():
    """ Attributes """
    def __init__(self):
        pygame.init()
        self.login = True
        self.running = False
        self.playing = False
        self.register = False
        self.signin = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.RIGHT_KEY = False
        self.LEFT_KEY = False
        self.UNICODE_KEY = False
        self.DISPLAY_W = 480*1.5
        self.DISPLAY_H = 270*1.5 #remoed times 2
        self.MAZE_W = 364
        self.MAZE_H = 403
        self.PLAYER_START = vec(1,1)
        self.CELL_W = self.MAZE_W // 28
        self.CELL_H = self.MAZE_H // 30
        self.unicode_text = ''
        self.display = pygame.display.set_mode((self.DISPLAY_H, self.DISPLAY_W))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name_defult = pygame.font.Font(None, 20)   
        self.font_name_8bit = '8-BIT WONDER.TTF'
        self.font_name_pacmanio = 'PacmanioFont.TTF'
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.GREY = (107,107,107)
        self.main_menu = MainMenu(self)                                                                         #refrence main menu object
        self.register_menu = RegisterMenu(self)
        self.login_menu = StartUpMenu(self)                                                                        #enables current menu to be chanegd depenfin gon whats selected
        self.signin_menu = SignInMenu(self)
        self.player = Player(self, self.PLAYER_START)
        self.load()

    """ Methods """
    def check_events(self):
        """ Method to check whenever user enters a key """
        for event in pygame.event.get():      #goes through a list of everything player can do on computer
            if event.type == pygame.QUIT:       #checks if user closes window
                self.login = False
                self.intro = False
                self.running = False
                self.playing = False
                self.register = False
                self.signin = False
                self.login_menu.run_display = False
                self.register_menu.run_display = False
                self.main_menu.run_display = False
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
                    
    def reset_keys(self):  
        """ Method to reset keys """
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.LEFT_KEY = False
        self.RIGHT_KEY = False
        self.UNICODE_KEY = False

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

        