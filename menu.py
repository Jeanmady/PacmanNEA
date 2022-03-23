import pygame
from databse import * 

class Menu():
    """ Base Menu Class inherited by other Menus """
    """ Attributes """
    def __init__(self, game):
        self.game = game                                                                                   # Takes the game class attributes to make them accessible in the menu class
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2                          # Cakcukates and stores centre values in the display
        self.run_display = True                                                                            # Boolean variab;e used in method display_menu
        self.cursor_rect_left = pygame.Rect(0,0,20,20)                                                     # 20 by 20 square as a cursor for left hand side
        self.offset_left = -150                                                                            # moves cursor to the left
        self.cursor_rect_right = pygame.Rect(0,0,20,20)                                                    # 20 by 20 square as a cursor for right hand side
        self.offset_right = 150                                                                            # moves cursor to the right
        self.inp_username = ''
        self.inp_pass = ''
        self.inp_repass = ''
        self.hidden_pass = ''
        self.hidden_repass = ''
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

class LoginMenu(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)                                                                          # gets all variables from menu class
        self.state = "Login"                                                                               # sets initial position of cursour to be login as its the fisrt item
        self.loginx, self.loginy = self.mid_w, self.mid_h + 10
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
        self.move_cursors()
        if self.game.START_KEY:
            if self.state == 'Login':
                self.game.signin = True
                self.game.intro = False
                self.game.running = False
                self.game.playing = False
                self.game.register = False
                self.game.login = False
               #add: to after signin self.game.running = True    #here shoud add functions to do with the login proccesss
            elif self.state == 'Register':
                self.game.signin = False
                self.game.intro = False
                self.game.running = False
                self.game.playing = False
                self.game.register = True
                self.game.login = False
            elif self.state == 'Exit':
                self.game.login = False
                self.game.intro = False
                self.game.running = False
                self.game.playing = False
                self.game.register = False
                self.game.signin = False
                self.game.login_menu.run_display = False
                self.game.register_menu.run_display = False
                self.game.main_menu.run_display = False
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
                self.DatabaseActions.check_login()
                """self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
                self.game.login = False
                self.game.intro = False
                self.game.running = True
                self.game.playing = False
                self.game.register = False
                self.game.signin = False"""
            elif self.state == 'Exit':
                self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
                self.game.login = True
                self.game.intro = True
                self.game.running = False
                self.game.playing = False
                self.game.register = False
                self.game.signin = False
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
                self.DatabaseActions.create_username()
                """self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
                pass"""
            elif self.state == 'Exit':
                self.game.intro = False
                self.game.running = False
                self.game.playing = False
                self.game.register = False
                self.game.login = True
                self.inp_pass = ''
                self.inp_username = ''
                self.inp_repass = ''
            self.run_display = False

class MainMenu(Menu):
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
            self.game.draw_text('Highscore', 15, 75,10)
            #highscore acc score here
            self.game.draw_text_8bit('Main Menu', 20, self.mid_w, self.mid_h - 20)
            self.game.draw_text_8bit("Begin Game", 20, self.startx, self.starty)
            self.game.draw_text_8bit("Game Controls", 20, self.controlsx, self.controlsy)
            self.game.draw_text_8bit("Add Friends", 20, self.friendsx, self.friendsy)
            self.game.draw_text_8bit("Score Boards", 20, self.boardsx, self.boardsy)
            self.game.draw_text_8bit("Exit Game", 20, self.exitx, self.exity)
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
                
                self.game.playing = True
            elif self.state == 'Controls':
                pass
            elif self.state == 'Friends':
                pass
            elif self.state == 'Boards':
                pass
            elif self.state == 'Exit':
                self.game.intro, self.game.running, self.game.playing, self.game.register, self.game.login = False, False, False, False, False
            self.run_display = False

class GameControls(Menu):
    """ Attributes """
    def __init__(self, game):
        Menu.__init__(self, game)
    
