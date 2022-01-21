import pygame
import sys
import os


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


class TicTacToe:
    pl1 = pl2 = 0

    # создание поля
    def __init__(self, scr):
        directory = os.getcwd()
        self.click_run = None
        self.field = [[415, 578, 741, 221], [415, 578, 741, 384], [415, 578, 741, 547]]
        self.board = [[None for i in range(3)] for i in range(3)]
        self.player = True
        self.moves = 0
        self.scr = scr
        self.ttt_font = pygame.font.Font("games\\tic_tac_toe\\fonts\\Troubleside.ttf", 80)
        scr.fill((155, 155, 155))
        self.render(scr)
        self.winner_run = False
        self.click_run = False
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_cell(event.pos)
            pygame.display.flip()
            self.winner_fin(scr)
            self.click_to_con(scr)

    def render(self, scr, mode="continue", direction=None, line=None, player=None):
        scr.fill((155, 155, 155))
        pygame.draw.rect(scr, (0, 0, 0), (0, 0, 1280, 100))
        scr.blit(self.ttt_font.render(f"Player1 - {self.pl1}", 1, (0, 0, 153)), (38, -10))
        scr.blit(self.ttt_font.render(f"Player2 - {self.pl2}", 1, (200, 9, 2)), (676, -10))
        scr.blit(load_image("games\\tic_tac_toe\\images\\field.png", -1), (412, 208))
        if self.player:
            scr.blit(load_image("games\\tic_tac_toe\\images\\x.png", -1), (10, 110))
        else:
            scr.blit(load_image("games\\tic_tac_toe\\images\\o.png", -1), (10, 110))
        for y in range(3):
            for x in range(3):
                if self.board[y][x]:
                    scr.blit(load_image("games\\tic_tac_toe\\images\\x.png", -1), (self.field[y][x] + 5, self.field[y][3] + 5))
                elif self.board[y][x] is False:
                    scr.blit(load_image("games\\tic_tac_toe\\images\\o.png", -1), (self.field[y][x] + 5, self.field[y][3] + 5))
        if mode == "stop":
            color = self.get_player_color(player)
            if direction == "hor":
                scr.blit(pygame.transform.rotate(load_image(f"games\\tic_tac_toe\\images\\line1_{color}.png", -1), 90), (422, 262 + line * 163))
            elif direction == "vert":
                scr.blit(load_image(f"games\\tic_tac_toe\\images\\line1_{color}.png", -1), (461 + line * 163, 226))
            elif direction == "diag" and line == 2:
                scr.blit(pygame.transform.flip(load_image(f"games\\tic_tac_toe\\images\\line2_{color}.png", -1), True, False), (432, 228))
            elif direction == "diag" and line == 1:
                scr.blit(load_image(f"games\\tic_tac_toe\\images\\line2_{color}.png", -1), (432, 228))
            if self.pl1 == 10 or self.pl2 == 10:
                self.winner_run = True
            else:
                self.click_run = True
        if self.moves == 9:
            self.click_run = True

    def click_to_con(self, scr):
        while self.click_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_run = False
                    self.__init__(scr)

    def winner_fin(self, scr):
        if self.winner_run:
            self.render_reset(scr)
        while self.winner_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.pl1 = self.pl2 = 0
                    self.winner_run = False
                    self.__init__(scr)
            pygame.display.flip()

    def render_reset(self, scr):
        scr.fill((155, 155, 155))
        pygame.draw.rect(scr, (0, 0, 0), (0, 0, 1280, 100))
        scr.blit(self.ttt_font.render(f"Player1 - {self.pl1}", 1, (0, 0, 153)), (38, -10))
        scr.blit(self.ttt_font.render(f"Player2 - {self.pl2}", 1, (200, 9, 2)), (676, -10))
        font_l = pygame.font.Font("games\\tic_tac_toe\\fonts\\Troubleside.ttf", 12)
        if self.pl1 > self.pl2:
            scr.blit(self.ttt_font.render("PLayer1 won", 1, (0, 0, 153)), (365, 346))
        else:
            scr.blit(self.ttt_font.render("PLayer2 won", 1, (200, 9, 2)), (365, 346))
        scr.blit(font_l.render("Нажмите любую кнопку, чтобы начать заново", 1, (0, 0, 0)), (473, 488))

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
                    self.moves += 1
        for i in range(3):
            if self.board[i].count(self.board[i][0]) == len(self.board[i]) and self.board[i][0] is not None:
                self.render(self.scr, mode="stop", direction="hor", line=i, player=self.board[i][0])
                return
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                self.render(self.scr, mode="stop", direction="vert", line=i, player=self.board[1][i])
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] is not None:
            self.render(self.scr, mode="stop", direction="diag", line=1, player=self.board[1][1])
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] is not None:
            self.render(self.scr, mode="stop", direction="diag", line=2, player=self.board[1][1])
        else:
            self.render(self.scr)

    def get_player_color(self, player=None):
        if player:
            self.pl1 += 1
            return "blue"
        else:
            self.pl2 += 1
            return "red"



