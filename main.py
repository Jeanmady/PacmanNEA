from game import Game

g = Game()
while g.login:
    g.login_menu.display_menu()
while g.register:
    g.register_menu.display_menu()
while g.signin:
    g.signin_menu.display_menu()   
while g.running:
    g.main_menu.display_menu()
    g.game_loop()