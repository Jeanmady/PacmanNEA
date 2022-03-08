import pygame



class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.DISPLAY_W = 480
        self.DISPLAY_H = 270
        self.display = pygame.display.set_mode((self.DISPLAY_H, self.DISPLAY_W))
        self.font_name = pygame.font.get_default_font()    #vhange later
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)

    def check_events(self):
        for events in pygame.event.get():  #goes through a list of everything player can do on computer
            if event.type == pygame.QUIT:  #checks if user closes window
                 self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:  #checks if user presses something on keyboard
                if event.key == pygame.K_RETURN:
                    gggg