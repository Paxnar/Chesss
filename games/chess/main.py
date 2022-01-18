import pygame
import sys
import os

WHITE = 1
BLACK = 2
selected = 'none'


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
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), None, None, None,
            King(WHITE), None, None, Rook(WHITE)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]


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
            print('1')
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            print(self.color)
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


class Rook:

    def __init__(self, color):
        self.color = color
        self.castling = True

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
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


class Pawn:

    def __init__(self, color):
        self.color = color

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


class Knight:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.get_color():
            return False

        if (abs(row1 - row) == 2 and abs(col1 - col) == 1) or (abs(row1 - row) == 1 and abs(col1 - col) == 2):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.castling = True
        self.castling2 = False

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
                    if board.field[row][7].castling:
                        self.castling2 = True
                    else:
                        return False
            elif col1 == 2 and row == row1 and col - col1 == 2:
                if type(board.field[row][0]) != Rook or board.field[row][1] is not None \
                        or board.field[row][3] is not None:
                    return False
                else:
                    if board.field[row][0].castling:
                        self.castling2 = True
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
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    '''Класс ферзя. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

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


class Bishop:
    def __init__(self, color):
        self.color = color

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
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 280
        self.top = 0
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, field):
        x = self.left
        y = self.top
        size = self.cell_size
        for i in range(len(field)):
            for o in range(len(field[i])):
                if type(field[i][o]) == Queen:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wQueen.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bQueen.png"), (90, 90))
                    screen.blit(image, (280 + 90 * o, 90 * (7 - i)))
                elif type(field[i][o]) == King:
                    if field[i][o].get_color() == WHITE:
                        image = pygame.transform.scale(load_image("wKing.png"), (90, 90))
                    else:
                        image = pygame.transform.scale(load_image("bKing.png"), (90, 90))
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
        global selected
        print(selected)
        if cell_coords is not None:
            if selected == 'none' and board.field[7 - cell_coords[1]][cell_coords[0]] is not None:
                selected = 'piece'
                self.piece_coords = cell_coords
            elif selected == 'piece':
                selected = 'none'
                if board.move_piece(7 - self.piece_coords[1], self.piece_coords[0], 7 - cell_coords[1], cell_coords[0]):
                    print(True)
                else:
                    print(False)


def main():
    # Создаём шахматную доску
    chisla = [720, 8]
    board = Board()
    pygame.init()
    pygame.display.set_caption('Шахматы')
    size = width, height = 1280, int(chisla[0])
    screen = pygame.display.set_mode(size)
    boardpygame = BoardPygame(8, 8)
    boardpygame.cell_size = chisla[0] // chisla[1]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill(pygame.Color(155, 155, 155))
            draw(screen, int(chisla[1]))
            boardpygame.render(screen, board.field)
            pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boardpygame.get_click(event.pos, screen, board)
    pygame.quit()



if __name__ == "__main__":
    main()
