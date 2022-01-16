import os
import pygame
import sys


class Menu:
    def __init__(self, menu_items=[(396, 319), (305, 93), "Item", (0, 0, 0), (18, 0, 255), 0]):
        self.menu_items = menu_items

    # рендер каждого пункта
    def render(self, scr, font, active_item):
        for i in self.menu_items:
            if i[5] == active_item:
                scr.blit(font.render(i[2], 1, i[4]), i[0])
            else:
                scr.blit(font.render(i[2], 1, i[3]), i[0])

    # цикл меню
    def menu_cyc(self):
        run = True
        menu_font = pygame.font.Font("fonts\\Arial.otf", 80)

        while run:
            screen.fill((0, 0, 0))
            screen.blit(pygame.image.load("images\\background.jpg"), (0, 0))
            item = -1
            mouse_pos = pygame.mouse.get_pos()
            for i in self.menu_items:
                if i[0][0] + i[1][0] > mouse_pos[0] > i[0][0] and i[0][1] + i[1][1] > mouse_pos[1] > i[0][1]:
                    item = i[5]
            self.render(screen, menu_font, item)

            for menu_event in pygame.event.get():
                if menu_event.type == pygame.QUIT:
                    sys.exit()
                if menu_event.type == pygame.MOUSEBUTTONDOWN and menu_event.button == 1:
                    if item == 0:
                        run = False
                    if item == 1:
                        run = False
                    elif item == 2:
                        sys.exit()
            pygame.display.flip()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


items = [((483, 200), (305, 93), "Играть", (0, 0, 0), (18, 0, 255), 0),
         ((396, 310), (486, 93), "Настройки", (0, 0, 0), (18, 0, 255), 1),
         ((494, 420), (289, 93), "Выйти", (0, 0, 0), (18, 0, 255), 2)]

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
menu = Menu(items)
menu.menu_cyc()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
pygame.quit()
