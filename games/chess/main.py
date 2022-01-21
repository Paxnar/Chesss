import pygame
import sys
import os
from random import randint

WHITE = 1
BLACK = 2
checkW = False
checkB = False


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        self.kingscoords = [[0, 4], [7, 4]]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            print('coords')
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            if self.color == WHITE:
                print('WHITE')
            else:
                print('BLACK')
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if type(self.field[row1][col1]) == Pawn:
            if (piece.get_color() == WHITE and row1 == 7) or (piece.get_color() == BLACK and row1 == 0):
                self.field[row1][col1] = Queen(piece.get_color())
        if type(self.field[row1][col1]) == King:
            if not self.field[row1][col1].castling:
                if self.field[row1][col1].castling2:
                    if col1 == 6:
                        piece = self.field[row1][7]
                        self.field[row1][7] = None
                        self.field[row1][5] = piece
                    elif col1 == 2:
                        piece = self.field[row1][0]
                        self.field[row1][0] = None
                        self.field[row1][3] = piece
        self.color = opponent(self.color)
        return True


class Piece:
    def __init__(self):
        self.exists = True

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class Rook(Piece):

    def __init__(self, color):
        self.color = color
        self.castling = True
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if board.get_piece(row1, col1) is not None:
            if board.get_piece(row1, col1).get_color() == self.color:
                return False
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        self.castling = False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class Pawn(Piece):

    def __init__(self, color):
        self.color = color
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class Knight(Piece):

    def __init__(self, color):
        self.color = color
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        piece1 = board.get_piece(row1, col1)
        if piece1 is not None and piece1.get_color() == self.get_color():
            return False

        if (abs(row1 - row) == 2 and abs(col1 - col) == 1) or (abs(row1 - row) == 1 and abs(col1 - col) == 2):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class King(Piece):
    def __init__(self, color):
        self.color = color
        self.castling = True
        self.castling2 = False
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        self.castling2 = False
        if not correct_coords(row1, col1):
            return False

        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.get_color():
            return False

        if self.castling:
            if col1 == 6 and row == row1 and col1 - col == 2:
                if type(board.field[row][7]) != Rook or board.field[row][5] is not None:
                    return False
                else:
                    if (self.color == WHITE and not checkW) or \
                            (self.color == BLACK and not checkB):
                        if board.field[row][7].castling:
                            self.castling2 = True
                        else:
                            return False
                    else:
                        return False
            elif col1 == 2 and row == row1 and col - col1 == 2:
                if type(board.field[row][0]) != Rook or board.field[row][1] is not None \
                        or board.field[row][3] is not None:
                    return False
                else:
                    if (self.color == WHITE and not checkW) or \
                            (self.color == BLACK and not checkB):
                        if board.field[row][0].castling:
                            self.castling2 = True
                        else:
                            return False
                    else:
                        return False

        if not ((col == col1)
                or (row == row1) or
                (abs(col - col1) == abs(row - row1))) and not self.castling2:
            return False

        if col == col1 and not self.castling2:
            if abs(row - row1) != 1:
                return False

        if row1 == row and not self.castling2:
            if abs(col - col1) != 1:
                return False

        if abs(col - col1) == abs(row - row1) and not self.castling2:
            if abs(col - col1) != 1:
                return False

        self.castling = False
        if self.color == WHITE:
            board.kingscoords[0] = [row1, col1]
        else:
            board.kingscoords[1] = [row1, col1]
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, color):
        self.color = color
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.get_color():
            return False

        if not ((col == col1)
                or (row == row1) or
                (abs(col - col1) == abs(row - row1))):
            return False

        if col == col1:
            step = (row1 - row) // abs(row1 - row)
            for i in range(1, abs(row1 - row)):
                row_check = row + i * step
                if board.get_piece(row_check, col):
                    return False

        if row1 == row:
            step = (col1 - col) // abs(col - col1)
            for i in range(1, abs(col - col1)):
                col_check = col + i * step
                if board.get_piece(row, col_check):
                    return False

        if abs(col - col1) == abs(row - row1):
            step_row = (row1 - row) // abs(row - row1)
            step_col = (col1 - col) // abs(col - col1)
            for i in range(1, abs(row - row1)):
                row_check = row + i * step_row
                col_check = col + i * step_col
                if board.get_piece(row_check, col_check):
                    return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, color):
        self.color = color
        super().__init__()

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.get_color():
            return False

        if not abs(col - col1) == abs(row - row1):
            return False

        if abs(col - col1) == abs(row - row1):
            step_row = (row1 - row) // abs(row - row1)
            step_col = (col1 - col) // abs(col - col1)
            for i in range(1, abs(row - row1)):
                row_check = row + i * step_row
                col_check = col + i * step_col
                if board.get_piece(row_check, col_check):
                    return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def doesexist(self):
        if self.exists:
            return True
        else:
            return False


def draw(screen, much):
    x = 280
    y = 0
    size = screen.get_height() // much
    if much % 2 != 0:
        color = pygame.Color('black')
        starter = color
    else:
        color = pygame.Color('white')
        starter = color
    for i in range(much):
        for o in range(much):
            pygame.draw.rect(screen, color, (x, y, size, size), 0)
            x += size
            if color == pygame.Color('black'):
                color = pygame.Color('white')
            else:
                color = pygame.Color('black')
        if starter == pygame.Color('black'):
            starter = pygame.Color('white')
            color = pygame.Color('white')
        else:
            starter = pygame.Color('black')
            color = pygame.Color('black')
        x = 280
        y += size


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class BoardPygame:
    # создание поля
    def __init__(self, width, height):
        self.checkB = False
        self.checkW = False
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 280
        self.top = 0
        self.cell_size = 30
        self.selected = 'none'

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, field, board):
        x = self.left
        y = self.top
        size = self.cell_size
        self.checkB = False
        self.checkW = False
        whiteking = board.kingscoords[0]
        blackking = board.kingscoords[1]
        for i in range(len(field)):
            for o in range(len(field[i])):
                if field[i][o] is not None:
                    if field[i][o].can_attack(board, i, o, whiteking[0], whiteking[1]):
                        if field[i][o].get_color() != WHITE:
                            self.checkW = True
                    if field[i][o].can_attack(board, i, o, blackking[0], blackking[1]):
                        if field[i][o].get_color() != BLACK:
                            self.checkB = True
                    if self.checkW or self.checkB:
                        break
                    if not field[i][o].can_attack(board, i, o, whiteking[0], whiteking[1]) and \
                            not field[i][o].can_attack(board, i, o, blackking[0], blackking[1]):
                        self.checkB = False
                        self.checkW = False
        for i in range(len(field)):
            for o in range(len(field[i])):
                if field[i][o] is not None:
                    if not field[i][o].doesexist():
                        continue
                if type(field[i][o]) == Queen:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wQueen.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bQueen.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == King:
                    if field[i][o].get_color() == WHITE and not self.checkW:
                        image = pygame.transform.scale(load_image("wKing.png"), (90, 90))
                    elif field[i][o].get_color() == WHITE and self.checkW:
                        image = pygame.transform.scale(load_image("wKingshah.png"), (90, 90))
                    elif field[i][o].get_color() == BLACK and not self.checkB:
                        image = pygame.transform.scale(load_image("bKing.png"), (90, 90))
                    elif field[i][o].get_color() == BLACK and self.checkB:
                        image = pygame.transform.scale(load_image("bKingshah.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == Pawn:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wPawn.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bPawn.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == Bishop:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wBishop.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bBishop.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == Knight:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wKnight.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bKnight.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == Rook:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wRook.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bRook.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                x += size
            y += size
            x = self.left

    def get_click(self, mouse_pos, screen, board):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, screen, board)

    def get_cell(self, mouse_pos):
        mx = mouse_pos[0]
        my = mouse_pos[1]
        if mx not in range(self.left, self.left + self.cell_size * self.width + 1) or my not in range(self.top,
                                                                                                      self.top + self.cell_size * self.height + 1):
            return None
        else:
            return ((mx - self.left) // self.cell_size, (my - self.top) // self.cell_size)

    def on_click(self, cell_coords, screen, board):
        print(self.selected)
        if cell_coords is not None:
            if self.selected == 'none' and board.field[7 - cell_coords[1]][cell_coords[0]] is not None:
                self.movingpiece = board.field[7 - cell_coords[1]][cell_coords[0]]
                self.selected = 'piece'
                self.piece_coords = cell_coords
                board.field[7 - cell_coords[1]][cell_coords[0]].exists = False
                sound1 = pygame.mixer.Sound('data/piece_up.ogg')
                pygame.mixer.Sound.play(sound1)
            elif self.selected == 'piece':
                self.selected = 'none'
                if board.move_piece(7 - self.piece_coords[1], self.piece_coords[0], 7 - cell_coords[1], cell_coords[0]):
                    print(True)
                    board.field[7 - cell_coords[1]][cell_coords[0]].exists = True
                    sound1 = pygame.mixer.Sound('data/piece_down' + str(randint(1, 3)) + '.ogg')
                    pygame.mixer.Sound.play(sound1)
                else:
                    print(False)
                    board.field[7 - self.piece_coords[1]][self.piece_coords[0]].exists = True
                    sound1 = pygame.mixer.Sound('data/piece_up.ogg')
                    pygame.mixer.Sound.play(sound1)


def start_screen(screen, color, y=0, vertical=False):
    font = pygame.font.Font(None, 30)
    if not vertical:
        intro_text = ["a", "b", "c", "d", "e", 'f', 'g', 'h']
        text_coord = 280 - 88 // 2
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 88
            intro_rect.x = text_coord
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)
            if color == 'black':
                color = 'white'
            else:
                color = 'black'
    else:
        intro_text = ["8", "7", "6", "5", "4", '3', '2', '1']
        text_coord = -45
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 88
            intro_rect.y = text_coord
            intro_rect.x = y
            screen.blit(string_rendered, intro_rect)
            if color == 'black':
                color = 'white'
            else:
                color = 'black'

def main():
    # Создаём шахматную доску
    global checkB
    global checkW
    chisla = [720, 8]
    pygame.init()
    pygame.display.set_caption('Шахматы')
    size = width, height = 1280, int(chisla[0])
    screen = pygame.display.set_mode(size)
    boardpygame = BoardPygame(8, 8)
    board = Board()
    boardpygame.cell_size = chisla[0] // chisla[1]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill(pygame.Color(155, 155, 155))
            draw(screen, int(chisla[1]))
            boardpygame.render(screen, board.field, board)
            start_screen(screen, 'black', -2)
            start_screen(screen, 'white', 700)
            start_screen(screen, 'black', 280, vertical=True)
            start_screen(screen, 'white', 986, vertical=True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                boardpygame.get_click(event.pos, screen, board)
            if event.type == pygame.MOUSEMOTION and boardpygame.selected == 'piece':
                if type(boardpygame.movingpiece) == Queen:
                    if boardpygame.movingpiece.get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wQueen.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bQueen.png"), (90, 90))
                elif type(boardpygame.movingpiece) == King:
                    if boardpygame.movingpiece.get_color() == WHITE and not boardpygame.checkW:
                        image = pygame.transform.scale(load_image("wKing.png"), (90, 90))
                    elif boardpygame.movingpiece.get_color() == WHITE and boardpygame.checkW:
                        image = pygame.transform.scale(load_image("wKingshah.png"), (90, 90))
                    elif boardpygame.movingpiece.get_color() == BLACK and not boardpygame.checkB:
                        image = pygame.transform.scale(load_image("bKing.png"), (90, 90))
                    elif boardpygame.movingpiece.get_color() == BLACK and boardpygame.checkB:
                        image = pygame.transform.scale(load_image("bKingshah.png"), (90, 90))
                elif type(boardpygame.movingpiece) == Pawn:
                    if boardpygame.movingpiece.get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wPawn.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bPawn.png"), (90, 90))
                elif type(boardpygame.movingpiece) == Bishop:
                    if boardpygame.movingpiece.get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wBishop.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bBishop.png"), (90, 90))
                elif type(boardpygame.movingpiece) == Knight:
                    if boardpygame.movingpiece.get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wKnight.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bKnight.png"), (90, 90))
                elif type(boardpygame.movingpiece) == Rook:
                    if boardpygame.movingpiece.get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wRook.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bRook.png"), (90, 90))
                screen.blit(image, (event.pos[0] - 45, event.pos[1] - 45))
            pygame.display.flip()
            checkW = boardpygame.checkW
            checkB = boardpygame.checkB
    pygame.quit()


if __name__ == "__main__":
    main()
