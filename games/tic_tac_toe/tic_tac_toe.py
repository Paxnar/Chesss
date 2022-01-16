import pygame
import sys


def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
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


class Field:
    # создание поля
    def __init__(self, scr):
        self.field = [[415, 578, 741, 221], [415, 578, 741, 384], [415, 578, 741, 547]]
        self.board = [[None for i in range(3)] for i in range(3)]
        self.player = True
        self.scr = scr
        screen.fill((155, 155, 155))
        self.render(screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_cell(event.pos)
            pygame.display.flip()
        sys.exit()

    def render(self, scr, mode="continue", direction=None, line=None, player=None):
        for y in range(3):
            for x in range(3):
                pygame.draw.rect(screen, "red", (self.field[y][x], self.field[y][3], 120, 120))
                if self.board[y][x]:
                    scr.blit(load_image("images\\x.png"), (self.field[y][x], self.field[y][3]))
                elif self.board[y][x] is False:
                    scr.blit(load_image("images\\o.png", -1), (self.field[y][x], self.field[y][3]))
        if mode == "stop":
            color = self.get_player_color(player)
            if direction == "hor":
                scr.blit(pygame.transform.rotate(load_image(f"images\\line1_{color}.png", -1), 90), (422, 262 + line * 163))
            elif direction == "vert":
                scr.blit(load_image(f"images\\line1_{color}.png", -1), (461 + line * 163, 226))
            elif direction == "diag" and line == 1:
                scr.blit(pygame.transform.flip(load_image(f"images\\line2_{color}.png", -1), True, False), (432, 228))
            elif direction == "diag" and line == 2:
                scr.blit(load_image(f"images\\line2_{color}.png", -1), (432, 228))
            self.__init__(scr)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < 416 or mouse_pos[1] < 208 or mouse_pos[0] > 861 or mouse_pos[1] > 667:
            print(None)
            return
        for i in range(3):
            for f in range(3):
                if self.field[i][f] + 120 > mouse_pos[0] > self.field[i][f] and self.field[i][3] + 120 > \
                        mouse_pos[1] > self.field[i][3] and self.board[i][f] is None:
                    self.board[i][f] = self.player
                    self.player = not self.player
        for i in range(3):
            if self.board[i].count(self.board[i][0]) == len(self.board[i]) and self.board[i][0] is not None:
                self.render(self.scr, mode="stop", direction="hor", line=i, player=self.board[i][0])
                return
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                self.render(self.scr, mode="stop", direction="vert", line=i, player=self.board[i][0])
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] is not None:
            self.render(self.scr, mode="stop", direction="diag", line=1, player=self.board[1][0])
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] is not None:
            self.render(self.scr, mode="stop", direction="diag", line=2, player=self.board[1][0])
        else:
            self.render(self.scr)

    def get_player_color(self, player=None):
        if player:
            return "blue"
        else:
            return "red"


pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
field = Field(screen)
pygame.quit()
