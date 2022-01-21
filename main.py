
import pygame
import sys


class Menu:
    def __init__(self, menu_items=None, menu_games=None):
        if menu_games is None:
            menu_games = [[(41, "images\\test.png"), 127]]
        if menu_items is None:
            menu_items = [(396, 319), (305, 93), "Item", (0, 0, 0), (18, 0, 255), 0]
        self.menu_items = menu_items
        self.menu_games = menu_games

    # рендер каждого пункта
    def render_items(self, scr, font, active_item):
        for i in self.menu_items:
            if i[5] == active_item:
                scr.blit(font.render(i[2], 1, i[4]), i[0])
            else:
                scr.blit(font.render(i[2], 1, i[3]), i[0])

    def render_games(self, scr):
        for i in self.menu_games:
            for f in range(len(i) - 1):
                pygame.draw.rect(scr, (0, 0, 153), (i[f][0], i[-1], 272, 179), border_radius=25)
                screen.blit(pygame.image.load(i[f][1]), (i[f][0] + 22, i[-1] + 15))

    # цикл меню
    def menu_cyc(self):
        run = True
        menu_font = pygame.font.Font("fonts\\Arial.otf", 80)
        menu_section = "items"
        while run:
            screen.fill((0, 0, 0))
            screen.blit(pygame.image.load("images\\background.jpg"), (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            if menu_section == "items":
                item = -1
                for i in self.menu_items:
                    if i[0][0] + i[1][0] > mouse_pos[0] > i[0][0] and i[0][1] + i[1][1] > mouse_pos[1] > i[0][1]:
                        item = i[5]
                self.render_items(screen, menu_font, item)
                for menu_event in pygame.event.get():
                    if menu_event.type == pygame.QUIT:
                        sys.exit()
                    if menu_event.type == pygame.MOUSEBUTTONDOWN and menu_event.button == 1:
                        if item == 0:
                            menu_section = "games"
                        if item == 1:
                            run = False
                        elif item == 2:
                            sys.exit()
            if menu_section == "games":
                self.render_games(screen)
                game = 0
                for games_event in pygame.event.get():
                    if games_event.type == pygame.QUIT:
                        sys.exit()
                    if games_event.type == pygame.MOUSEBUTTONDOWN and games_event.button == 1:
                        pass
            pygame.display.flip()


items = [((483, 200), (305, 93), "Играть", (0, 0, 0), (18, 0, 255), 0),
         ((396, 310), (486, 93), "Настройки", (0, 0, 0), (18, 0, 255), 1),
         ((494, 420), (289, 93), "Выйти", (0, 0, 0), (18, 0, 255), 2)]

games = [[(41, "images\\game_ttt.png"), (350, "images\\game_chess.png"), (659, "images\\test.png"),
          (968, "images\\test.png"), 127], [(41, "images\\test.png"), (350, "images\\test.png"),
                                            (659, "images\\test.png"), 413]]

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
menu = Menu(items, games)
menu.menu_cyc()
pygame.quit()
