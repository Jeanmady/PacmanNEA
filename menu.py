import pygame


class Menu():
    def __init__(self, game):
        self.game = game # so access to games variables are accesible
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect_left = pygame.Rect(0,0,20,20) #20 by 20 square as a cursor later add image l
        self.offset_left = -150 #moves cursor to the left
        self.cursor_rect_right = pygame.Rect(0,0,20,20) #20 by 20 square as a cursor later add image r
        self.offset_right = 150 #moves cursor to the right

    def draw_cursors(self):
        self.game.draw_text('*', 15, self.cursor_rect_left.x, self.cursor_rect_left.y)
        self.game.draw_text('*', 15, self.cursor_rect_right.x, self.cursor_rect_right.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0)) 
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
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
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.mid_w, self.mid_h - 20)
            self.game.draw_text("Begin Game", 20, self.startx, self.starty)
            self.game.draw_text("Game Controls", 20, self.controlsx, self.controlsy)
            self.game.draw_text("Add Friends", 20, self.friendsx, self.friendsy)
            self.game.draw_text("Score Boards", 20, self.boardsx, self.boardsy)
            self.game.draw_text("Exit Game", 20, self.exitx, self.exity)
            self.draw_cursors()
            self.blit_screen()

    def move_cursors(self):
        """Method moves cursor by:
            Checking state, 
            adjusting cursors, 
            then readjust state"""
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
                self.game.running, self.game.playing = False, False
            self.run_display = False

    
