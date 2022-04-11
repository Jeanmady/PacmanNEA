import pygame
from databse import * 
import time
from Current_score import *

class Menu():
    """ Base Menu Class inherited by other Menus """
    """ Attributes """
    def __init__(self, game):
        self.game = game      # Takes the game class attributes to make them accessible in the menu class
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2      # Cakcukates and stores centre values in the display
        self.run_display = True     # Boolean variab;e used in method display_menu
        self.cursor_rect_left = pygame.Rect(0,0,20,20)     # 20 by 20 square as a cursor for left hand side
        self.offset_left = -150     # moves cursor to the left
        self.cursor_rect_right = pygame.Rect(0,0,20,20)    # 20 by 20 square as a cursor for right hand side
        self.offset_right = 150    # moves cursor to the right
        self.inp_username = ''  # these are all the stores for inputs on different menus 
        self.inp_pass = ''
        self.inp_repass = ''
        self.hidden_pass = ''
        self.hidden_repass = ''
        self.inp_add_friend = ''
        self.DatabaseActions = DatabaseActions(self)

    """ Methods """
    def draw_cursors(self):
        """ Draws cursors onto the screen """
        self.game.draw_text_8bit('*', 15, self.cursor_rect_left.x, self.cursor_rect_left.y)
        self.game.draw_text_8bit('*', 15, self.cursor_rect_right.x, self.cursor_rect_right.y)

    def blit_screen(self):
        """ Resets and updates screen should be used in while loop to ensure constant renewal of screen """
        self.game.window.blit(self.game.display, (0,0)) 
        pygame.display.update()
        self.game.reset_keys()

class StartUpMenu(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)       # gets all variables from menu class using inheritance
        self.state = "Login"           # sets initial position of cursour to be login as its the fisrt item
        self.loginx, self.loginy = self.mid_w, self.mid_h + 10  # variables to help with positioning of text
        self.registerx, self.registery = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect_left.midtop = (self.loginx + self.offset_left, self.loginy)
        self.cursor_rect_right.midtop = (self.loginx + self.offset_right, self.loginy)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_Pacmanio('Pacmanio', 60, self.mid_w, self.mid_h / 2 )
            self.game.draw_text_8bit('Login', 20, self.loginx, self.loginy)
            self.game.draw_text_8bit("Register", 20, self.registerx, self.registery)
            self.game.draw_text_8bit("Exit", 20, self.exitx, self.exity)
            self.draw_cursors()
            self.blit_screen()

    def move_cursors(self):
        """Method moves cursor by:
            Checking state, 
            adjusting cursors, 
            then readjust state"""
        if self.game.DOWN_KEY:
            if self.state == 'Login':
                self.cursor_rect_left.midtop = (self.registerx + self.offset_left, self.registery)
                self.cursor_rect_right.midtop = (self.registerx + self.offset_right, self.registery)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect_left.midtop = (self.exitx + self.offset_left, self.exity)
                self.cursor_rect_right.midtop = (self.exitx + self.offset_right, self.exity)
                self.state = 'Exit'

        elif self.game.UP_KEY:
            if self.state == 'Exit':
                self.cursor_rect_left.midtop = (self.registerx + self.offset_left, self.registery)
                self.cursor_rect_right.midtop = (self.registerx + self.offset_right, self.registery)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect_left.midtop = (self.loginx + self.offset_left, self.loginy)
                self.cursor_rect_right.midtop = (self.loginx + self.offset_right, self.loginy)
                self.state = 'Login'

    def check_input(self):
        """ Checks for user input on keyboard """
        # helps keep knowledge of where the cursor is
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Login':
                self.game.mainstate = 'login'
            elif self.state == 'Register':
                self.game.mainstate = 'register'
            elif self.state == 'Exit':
                self.game.running = False
            self.run_display = False


class SignInMenu(Menu):
    """ Class to create Sign In sub Menu for Login Page """     
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Enter Username"
        self.usernamex, self.usernamey = self.mid_w, self.mid_h 
        self.passwordx, self.passwordy = self.mid_w, self.mid_h + 20
        self.loginx, self.loginy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect_left.midtop = (self.usernamex - 100 + self.offset_left, self.usernamey)
        self.cursor_rect_right.midtop = (self.usernamex + 40 + self.offset_right, self.usernamey)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_8bit('Enter Username', 15, self.usernamex - 100, self.usernamey)
            self.game.draw_text_8bit("Enter Password", 15, self.passwordx - 100, self.passwordy)
            self.game.draw_text_8bit("Login", 20, self.loginx, self.loginy)
            self.game.draw_text_8bit("Exit", 20, self.exitx, self.exity)
            self.game.draw_text_bottom_left(self.inp_username, 10, self.usernamex + 10, self.usernamey )
            self.game.draw_text_bottom_left(self.hidden_pass, 10, self.passwordx + 10, self.passwordy)
            self.draw_cursors()
            self.blit_screen()

    def move_cursors(self):
        """Method moves cursor by:
            Checking state, 
            adjusting cursors, 
            then readjust state"""
        if self.game.DOWN_KEY:
            if self.state == 'Enter Username':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Enter Password'
            elif self.state == 'Enter Password':
                self.cursor_rect_left.midtop = (self.loginx - 100 + self.offset_left, self.loginy)
                self.cursor_rect_right.midtop = (self.loginx + 40 + self.offset_right, self.loginy)
                self.state = 'Login'
            elif self.state == 'Login':
                self.cursor_rect_left.midtop = (self.exitx + self.offset_left, self.exity)
                self.cursor_rect_right.midtop = (self.exitx + self.offset_right, self.exity)
                self.state = 'Exit'

        elif self.game.UP_KEY:
            if self.state == 'Exit':
                self.cursor_rect_left.midtop = (self.loginx + self.offset_left, self.loginy)
                self.cursor_rect_right.midtop = (self.loginx + self.offset_right, self.loginy)
                self.state = 'Login'
            elif self.state == 'Login':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Enter Password'
            elif self.state == 'Enter Password':
                self.cursor_rect_left.midtop = (self.usernamex - 100 + self.offset_left, self.usernamey)
                self.cursor_rect_right.midtop = (self.usernamex + 40 + self.offset_right, self.usernamey)
                self.state = 'Enter Username'

        elif self.game.BACK_KEY:
                    if self.state == 'Enter Username':
                        self.inp_username = self.inp_username[:-1]
                    elif self.state == 'Enter Password':
                        self.inp_pass = self.inp_pass[:-1]
                        self.hidden_pass = self.hidden_pass[:-1]

        elif self.game.UNICODE_KEY:
            if self.state == 'Enter Username':
                self.inp_username += self.game.unicode_text
            elif self.state == 'Enter Password':
                self.inp_pass += self.game.unicode_text
                self.hidden_pass += '*'

    def check_input(self):
        """ Checks for user input on keyboard """
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Login':      # not exiting back rto login menu and not going to game once login is pressed
                #self.DatabaseActions.check_login()
                if self.DatabaseActions.check_login(self.inp_username, self.inp_pass) == True:
                    self.game.draw_text_8bit('Login Accepted', 15, self.usernamex , self.usernamey -100)
                    self.DatabaseActions.move_to_playing_database(self.inp_username, self.DatabaseActions.get_ID(self.inp_username), int(self.DatabaseActions.get_highscore(self.inp_username)))
                    self.blit_screen()
                    time.sleep(3)
                    self.inp_pass = ''
                    self.inp_username = ''
                    self.inp_repass = ''
                    self.game.mainstate = 'mainmenu'
            elif self.state == 'Exit':
                self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
                self.hidden_pass = ''
                self.hidden_repass = ''
                self.game.mainstate = 'startup'
            self.run_display = False
            

class RegisterMenu(Menu):
    """ Class to create Register Sub Menu for Login Menu Class """
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Enter Username"
        self.usernamex, self.usernamey = self.mid_w, self.mid_h 
        self.passwordx, self.passwordy = self.mid_w, self.mid_h + 20
        self.renterx, self.rentery = self.mid_w, self.mid_h + 40
        self.registerx, self.registery = self.mid_w, self.mid_h + 90
        self.exitx, self.exity = self.mid_w, self.mid_h + 110
        self.cursor_rect_left.midtop = (self.usernamex - 100 + self.offset_left, self.usernamey)
        self.cursor_rect_right.midtop = (self.usernamex + 40 + self.offset_right, self.usernamey)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_8bit('Enter Username', 15, self.usernamex - 100, self.usernamey)
            self.game.draw_text_8bit("Enter Password", 15, self.passwordx - 100, self.passwordy)
            self.game.draw_text_8bit("ReEnter Password", 15, self.renterx - 100, self.rentery)
            self.game.draw_text_8bit("Register", 20, self.registerx, self.registery)
            self.game.draw_text_8bit("Exit", 20, self.exitx, self.exity)
            self.game.draw_text_bottom_left(self.inp_username, 10, self.usernamex + 10, self.usernamey )
            self.game.draw_text_bottom_left(self.hidden_pass, 10, self.passwordx + 10, self.passwordy)
            self.game.draw_text_bottom_left(self.hidden_repass, 10, self.renterx + 25, self.rentery)
            self.draw_cursors()
            self.blit_screen()


    def move_cursors(self):
        """Method moves cursor by:
            Checking state, 
            adjusting cursors, 
            then readjust state"""
        if self.game.DOWN_KEY:
            if self.state == 'Enter Username':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Enter Password'
            elif self.state == 'Enter Password':
                self.cursor_rect_left.midtop = (self.renterx - 100 + self.offset_left, self.rentery)
                self.cursor_rect_right.midtop = (self.renterx + 40 + self.offset_right, self.rentery)
                self.state = 'ReEnter Password'
            elif self.state == 'ReEnter Password':
                self.cursor_rect_left.midtop = (self.registerx - 100 + self.offset_left, self.registery)
                self.cursor_rect_right.midtop = (self.registerx + 40 + self.offset_right, self.registery)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect_left.midtop = (self.exitx + self.offset_left, self.exity)
                self.cursor_rect_right.midtop = (self.exitx + self.offset_right, self.exity)
                self.state = 'Exit'

        elif self.game.UP_KEY:
            if self.state == 'Exit':
                self.cursor_rect_left.midtop = (self.registerx + self.offset_left, self.registery)
                self.cursor_rect_right.midtop = (self.registerx + self.offset_right, self.registery)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect_left.midtop = (self.renterx - 100 + self.offset_left, self.rentery)
                self.cursor_rect_right.midtop = (self.renterx + 40 + self.offset_right, self.rentery)
                self.state = 'ReEnter Password'
            elif self.state == 'ReEnter Password':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Enter Password'
            elif self.state == 'Enter Password':
                self.cursor_rect_left.midtop = (self.usernamex - 100 + self.offset_left, self.usernamey)
                self.cursor_rect_right.midtop = (self.usernamex + 40 + self.offset_right, self.usernamey)
                self.state = 'Enter Username'

        elif self.game.BACK_KEY:
                    if self.state == 'Enter Username':
                        self.inp_username = self.inp_username[:-1]
                    elif self.state == 'Enter Password':
                        self.inp_pass = self.inp_pass[:-1]
                        self.hidden_pass = self.hidden_pass[:-1]
                    elif self.state == 'ReEnter Password':
                        self.inp_repass = self.inp_repass[:-1]
                        self.hidden_repass = self.hidden_repass[:-1]

        elif self.game.UNICODE_KEY:
            if self.state == 'Enter Username':
                self.inp_username += self.game.unicode_text
            elif self.state == 'Enter Password':
                self.inp_pass += self.game.unicode_text
                self.hidden_pass += '*'
            elif self.state == 'ReEnter Password':
                self.inp_repass += self.game.unicode_text
                self.hidden_repass += '*'

    def check_input(self):
        """ Checks for user input on keyboard """
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Register':
                if self.DatabaseActions.create_username(self.inp_username, self.inp_pass, self.inp_repass):
                    self.inp_pass = ''
                    self.inp_username = ''
                    self.inp_repass = ''
                    self.game.mainstate = 'startup'
                #dfhsyhayh add sttuff to show regusetred
                
            elif self.state == 'Exit':
                self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
                self.hidden_pass = ''
                self.game.mainstate = 'startup'
            self.run_display = False

class MainMenu(Menu, DatabaseActions):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game) #gets all variables form menu class
        self.state = "Start" #so cursor points at start game 
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 50
        self.friendsx, self.friendsy = self.mid_w, self.mid_h + 70
        self.boardsx, self.boardsy = self.mid_w, self.mid_h + 90
        self.exitx, self.exity = self.mid_w, self.mid_h + 110
        self.cursor_rect_left.midtop = (self.startx + self.offset_left, self.starty)
        self.cursor_rect_right.midtop = (self.startx + self.offset_right, self.starty)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_Pacmanio('Pacmanio', 60, self.mid_w, self.mid_h / 2 )
            self.game.draw_text_bottom_left(('HIGHSCORE: {}').format(self.DatabaseActions.get_current_highscore()), 16, 5,10)
            self.game.draw_text_8bit('Main Menu', 20, self.mid_w, self.mid_h - 20)
            self.game.draw_text_8bit("Begin Game", 20, self.startx, self.starty)
            self.game.draw_text_8bit("Game Controls", 20, self.controlsx, self.controlsy)
            self.game.draw_text_8bit("Add Friends", 20, self.friendsx, self.friendsy)
            self.game.draw_text_8bit("Score Boards", 20, self.boardsx, self.boardsy)
            self.game.draw_text_8bit("Log out", 20, self.exitx, self.exity)
            self.draw_cursors()
            self.blit_screen()

    def move_cursors(self):
        """
            Method moves cursor by:
            Checking state
            Adjusting cursors
            Then re-adjust state
        """
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect_left.midtop = (self.controlsx + self.offset_left, self.controlsy)
                self.cursor_rect_right.midtop = (self.controlsx + self.offset_right, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect_left.midtop = (self.friendsx + self.offset_left, self.friendsy)
                self.cursor_rect_right.midtop = (self.friendsx + self.offset_right, self.friendsy)
                self.state = 'Friends'
            elif self.state == 'Friends':
                self.cursor_rect_left.midtop = (self.boardsx + self.offset_left, self.boardsy)
                self.cursor_rect_right.midtop = (self.boardsx + self.offset_right, self.boardsy)
                self.state = 'Boards'
            elif self.state == 'Boards':
                self.cursor_rect_left.midtop = (self.exitx + self.offset_left, self.exity)
                self.cursor_rect_right.midtop = (self.exitx + self.offset_right, self.exity)
                self.state = 'Exit'

        elif self.game.UP_KEY:
            if self.state == 'Exit':
                self.cursor_rect_left.midtop = (self.boardsx + self.offset_left, self.boardsy)
                self.cursor_rect_right.midtop = (self.boardsx + self.offset_right, self.boardsy)
                self.state = 'Boards'
            elif self.state == 'Boards':
                self.cursor_rect_left.midtop = (self.friendsx + self.offset_left, self.friendsy)
                self.cursor_rect_right.midtop = (self.friendsx + self.offset_right, self.friendsy)
                self.state = 'Friends'
            elif self.state == 'Friends':
                self.cursor_rect_left.midtop = (self.controlsx + self.offset_left, self.controlsy)
                self.cursor_rect_right.midtop = (self.controlsx + self.offset_right, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect_left.midtop = (self.startx + self.offset_left, self.starty)
                self.cursor_rect_right.midtop = (self.startx + self.offset_right, self.starty)
                self.state = 'Start'

    def check_input(self):
        """ Checks for user input on keyboard """
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.mainstate = 'playing'
            elif self.state == 'Controls':
                self.game.mainstate = 'controls'
            elif self.state == 'Friends':
                self.game.mainstate = 'addfriends'
            elif self.state == 'Boards':
                self.game.mainstate = 'boards'
            elif self.state == 'Exit':
                self.game.mainstate = 'startup'
            self.run_display = False

class GameOver(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game) #gets all variables form menu class
        self.state = "Start" #so cursor points at start game 
        self.gameoverx, self.gameovery = self.mid_w, self.mid_h + 10      
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect_left.midtop = (self.exitx + self.offset_left, self.exity)
        self.cursor_rect_right.midtop = (self.exitx + self.offset_right, self.exity)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_bottom_left(('HIGHSCORE: {}'.format(self.DatabaseActions.get_current_highscore())), 16, 5,10)
            self.game.draw_text_bottom_right(('SCORE: {}'.format(self.DatabaseActions.get_current_score())), 16, 595,10)
            self.game.draw_text_8bit('Game Over', 30, self.gameoverx, self.gameovery - 20)
            self.game.draw_text_8bit('Exit', 20, self.exitx, self.exity)
            self.draw_cursors()
            self.blit_screen()

    def check_input(self):
        """ Checks for user input on keyboard """
        if self.game.START_KEY:
            self.game.reset()
            self.game.mainstate = 'mainmenu'
            
            self.run_display = False


class GameControls(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start" #so cursor points at start game 
        self.startx, self.starty = self.mid_w, self.mid_h + 10
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 30
        self.friendsx, self.friendsy = self.mid_w, self.mid_h + 50
        self.boardsx, self.boardsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.superx, self.supery = self.mid_w, self.mid_h + 110
        self.stickyx, self.stickyy = self.mid_w, self.mid_h + 130
        self.cursor_rect_left.midtop = (self.startx + self.offset_left, self.starty)
        self.cursor_rect_right.midtop = (self.startx + self.offset_right, self.starty)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_Pacmanio('Pacmanio', 60, self.mid_w, (self.mid_h / 2) - 30 )
            self.game.draw_text_8bit('Controls', 20, self.mid_w, self.mid_h - 40)
            self.game.draw_text_8bit("arrow keys to move", 12, self.startx, self.starty)
            self.game.draw_text_8bit("plus 10 pts", 12, self.controlsx, self.controlsy)
            pygame.draw.circle(self.game.display, self.game.WHITE, (self.mid_w - 90, self.controlsy), 4)
            self.game.draw_text_8bit("plus one life", 12, self.friendsx, self.friendsy)
            pygame.draw.circle(self.game.display, self.game.RED, (self.mid_w-90, self.friendsy ), 7)
            self.game.draw_text_8bit("boosts you", 12, self.boardsx, self.boardsy)
            pygame.draw.circle(self.game.display, self.game.GREEN, (self.mid_w-90, self.boardsy ), 7)
            self.game.draw_text_8bit("run away from the ghosts", 12, self.exitx, self.exity)
            pygame.draw.circle(self.game.display, (234,130,229), (self.mid_w-150, self.exity ), 7)
            pygame.draw.circle(self.game.display, (70,191,238), (self.mid_w-170, self.exity ), 7)
            pygame.draw.circle(self.game.display, (208,62,25), (self.mid_w-190, self.exity ), 7)
            pygame.draw.circle(self.game.display, (219,133,28), (self.mid_w-210, self.exity ), 7)
            self.game.draw_text_8bit("eat ghosts after eating super pellets", 12, self.superx, self.supery)
            pygame.draw.circle(self.game.display, self.game.BABY_BLUE, (self.mid_w-220, self.supery ), 6)
            pygame.draw.circle(self.game.display, (0,0,139), (self.mid_w+220, self.supery ), 7)
            pygame.draw.circle(self.game.display, (0,0,139), (self.mid_w+240, self.supery ), 7)
            pygame.draw.circle(self.game.display, (0,0,139), (self.mid_w+260, self.supery ), 7)
            pygame.draw.circle(self.game.display, (0,0,139), (self.mid_w+280, self.supery ), 7)
            self.game.draw_text_8bit("walls are sticky do not hit", 12, self.stickyx, self.stickyy)
            self.game.draw_text_8bit("Press Enter to return", 12, self.stickyx, self.stickyy+ 20)
            self.blit_screen()


    def check_input(self):
        """ Checks for user input on keyboard """
        if self.game.START_KEY:
            self.game.mainstate = 'mainmenu'

            self.run_display = False


class AddFriends(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Enter FriendID"
        self.usernamex, self.usernamey = self.mid_w, self.mid_h 
        self.passwordx, self.passwordy = self.mid_w, self.mid_h + 20
        self.loginx, self.loginy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect_left.midtop = (self.usernamex - 100 + self.offset_left, self.usernamey)
        self.cursor_rect_right.midtop = (self.usernamex + 40 + self.offset_right, self.usernamey)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text_8bit('Enter FriendID', 15, self.usernamex - 100, self.usernamey)
            self.game.draw_text_8bit("Add Friend", 15, self.passwordx, self.passwordy)
            self.game.draw_text_8bit("Exit", 20, self.loginx, self.loginy)
            self.game.draw_text_bottom_left(self.inp_add_friend, 10, self.usernamex + 10, self.usernamey )
            self.draw_cursors()
            self.blit_screen()

    def move_cursors(self):
        """Method moves cursor by:
            Checking state, 
            adjusting cursors, 
            then readjust state"""
        if self.game.DOWN_KEY:
            if self.state == 'Enter FriendID':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Add Friend'
            elif self.state == 'Add Friend':
                self.cursor_rect_left.midtop = (self.loginx - 100 + self.offset_left, self.loginy)
                self.cursor_rect_right.midtop = (self.loginx + 40 + self.offset_right, self.loginy)
                self.state = 'Exit'

        elif self.game.UP_KEY:
            if self.state == 'Exit':
                self.cursor_rect_left.midtop = (self.loginx + self.offset_left, self.loginy)
                self.cursor_rect_right.midtop = (self.loginx + self.offset_right, self.loginy)
                self.state = 'Add Friend'
            elif self.state == 'Add Friend':
                self.cursor_rect_left.midtop = (self.passwordx - 100 + self.offset_left, self.passwordy)
                self.cursor_rect_right.midtop = (self.passwordx + 40 + self.offset_right, self.passwordy)
                self.state = 'Enter FriendID'

        elif self.game.BACK_KEY:
                    if self.state == 'Enter FriendID':
                        self.inp_add_friend = self.inp_add_friend[:-1]
                    

        elif self.game.UNICODE_KEY:
            if self.state == 'Enter FriendID':
                self.inp_add_friend += self.game.unicode_text

    def check_input(self):
        """ Checks for user input on keyboard """
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Add Friend':   
                if self.DatabaseActions.add_friend(self.DatabaseActions.get_current_userid(), self.inp_add_friend) == True:
                    self.game.draw_text_8bit('Friend added', 15, self.usernamex , self.usernamey -100)
                    self.blit_screen()
                    time.sleep(3)
                    self.inp_add_friend = ''
                    self.game.mainstate = 'mainmenu'
            elif self.state == 'Exit':
                self.inp_add_friend = ''
                self.game.mainstate = 'mainmenu'
            self.run_display = False
    
class ScoreBoards(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start" #so cursor points at start game 
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 50
        self.friendsx, self.friendsy = self.mid_w, self.mid_h + 70
        self.boardsx, self.boardsy = self.mid_w, self.mid_h + 90
        self.exitx, self.exity = self.mid_w, self.mid_h + 110
        self.cursor_rect_left.midtop = (self.startx + self.offset_left, self.starty)
        self.cursor_rect_right.midtop = (self.startx + self.offset_right, self.starty)

    def display_menu(self):
        """ Method to display Menu onto the screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            
            self.game.display.fill(self.game.BLACK)
            all_scores = self.game.get_highscores_dict(self.DatabaseActions.get_all_scores())
            for item in all_scores:
                    i = 0
                    while i< 10:
                        self.game.draw_text_8bit('{},{}'.format(item, all_scores[item]), 8, self.mid_w/2, (self.mid_h - 20)+40*i)
                        i+=1
            
            self.blit_screen()


    def check_input(self):
        """ Checks for user input on keyboard """
        if self.game.START_KEY:
            self.game.mainstate = 'mainmenu'
            self.run_display = False
    

    
    
