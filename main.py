from game import Game

g = Game()
g.curr_menu.display_menu()
while g.register:
    g.register_menu.display_menu()
while g.running:
    g.main_menu.display_menu()
    g.game_loop()