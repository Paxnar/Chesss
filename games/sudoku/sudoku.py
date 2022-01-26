from random import sample, choice
import pygame
from copy import deepcopy
import random



# pattern for a baseline valid solution
def mix(ran, n):
    x = (cells * (ran % cells) + ran // cells + n) % side
    print(x)
    return (cells * (ran % cells) + ran // cells + n) % side


# перемешивание доски: строк и столбцов

def shuffle(s):
    return sample(s, len(s))




def get_coor(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif


def instruction_viz():
    text1 = font2.render('НАЖМИТЕ С ДЛЯ ОЧИСТКИ, ВЫ МОЖЕТЕ СОЗДАТЬ СВОЙ УРОВЕНЬ', 1, (0, 0, 0))
    text2 = font2.render('ВВЕДИТЕ ЗНАЧЕНИЕ, ИЛИ НАЖМИТЕ ENTER ДЛЯ РЕШЕНИЯ', 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))


def change_cell():  # выделение ячейки
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif),
                         (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif),
                         ((x + i) * dif, y * dif + dif), 7)


def draw():
    for i in range(9):
        for j in range(9):
            if sud_desk[i][j] != 0:
                # цвета ячеек с цифрами
                pygame.draw.rect(screen, (208, 232, 253), (i * dif, j * dif, dif + 1, dif + 1))
                # Заполнение доски цифрами
                text1 = font1.render(str(sud_desk[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # рисование раздлительных линей
    for i in range(10):
        if i % 3 == 0:
            thick = 3
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)


# вставка введенного значения

def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# ошибка при неправильной цифре

def raise_error1():
    text1 = font_alert.render('НЕПРАВИЛЬНО! НАЧНИТЕ СНАЧАЛА!', 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def raise_error2():
    text1 = font_alert.render('НЕПРАВИЛЬНО! НЕВЕРНАЯ ЦИФРА!', 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def valid(m, i, j, val):  # является ли введеное значение верным
    for z in range(9):
        if m[i][z] == val:
            return False
        if m[z][j] == val:
            return False
    z = i // 3
    v = j // 3
    for i in range(z * 3, z * 3 + 3):
        for j in range(v * 3, v * 3 + 3):
            if m[i][j] == val:
                return False
    return True


def solve(sud_desk, i, j):  # решение Судоку
    while sud_desk[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for z in range(1, 10):
        if valid(sud_desk, i, j, z) == True:
            if valid(sud_desk, i, j, z):
                sud_desk[i][j] = z
                global x, y
                x = i
                y = j
                screen.fill((255, 255, 255))
                draw()
                change_cell()
                pygame.display.update()
                pygame.time.delay(20)
                if solve(sud_desk, i, j) == 1:
                    return True
                else:
                    sud_desk[i][j] = 0
                screen.fill((255, 255, 255))

                draw()
                change_cell()
                pygame.display.update()
                pygame.time.delay(50)
    return False


# Display options when solved


def result():
    text1 = font2.render('ПОЗДРАВЛЯЕМ!! закройте окно :3', 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

def main(scr):
    global cells, side, rBase, rows, cols, nums, board, squares, void, numSize, sud_desk, screen, x, y, dif, val, \
        grid_T, font1, font_alert, font2, run, flag1, flag2, res, error
    cells = 3
    side = cells * cells
    rBase = range(cells)
    rows = [g * cells + ran for g in shuffle(rBase) for ran in shuffle(rBase)]
    cols = [g * cells + n for g in shuffle(rBase) for n in shuffle(rBase)]
    nums = shuffle(range(1, cells * cells + 1))
    # создание доски
    board = [[nums[mix(ran, n)] for n in cols] for ran in rows]
    for line in board:
        print(line)
    squares = 81
    void = random.choice(range(50, 60))
    for p in sample(range(squares), void):
        board[p // side][p % side] = 0
    numSize = len(str(side))
    sud_desk = []
    for line in board:
        print(line)
        sud_desk.append(line)
    print(sud_desk)
    pygame.font.init()
    screen = scr
    x = 0
    y = 0
    dif = 500 / 9
    val = 0
    grid_T = deepcopy(sud_desk)
    font1 = pygame.font.SysFont("Helvetica", 40)
    font_alert = pygame.font.SysFont("Helvetica", 25)
    font_alert = pygame.font.SysFont("Helvetica", 22)
    font2 = pygame.font.SysFont("comicsans", 20)
    run = True
    flag1 = 0
    flag2 = 0
    res = 0
    error = 0

    while run:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # получение координат мыши для выбора ячейки
                flag1 = 1
                pos = pygame.mouse.get_pos()
                get_coor(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
                if event.key == pygame.K_RETURN:
                    flag2 = 1
                if event.key == pygame.K_LEFT:
                    if event.key == pygame.K_LEFT and x > 0:
                        x -= 1
                        flag1 = 1
                if event.key == pygame.K_RIGHT:
                    if event.key == pygame.K_RIGHT and x < 8:
                        x += 1
                        flag1 = 1
                if event.key == pygame.K_UP:
                    if event.key == pygame.K_UP and y > 0:
                        y -= 1
                        flag1 = 1
                if event.key == pygame.K_DOWN:
                    if event.key == pygame.K_DOWN and y < 8:
                        y += 1
                        flag1 = 1
                if event.key == pygame.K_r:
                    res = 0
                    error = 0
                    flag2 = 0
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_c:  # На кнопку C очистка всей доски (будет убрана)
                    res = 0
                    error = 0
                    flag2 = 0
                    sud_desk = [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]
                if event.key == pygame.K_d:  # для возвращения доски в начальное состояние
                    res = 0
                    error = 0
                    flag2 = 0
                    sud_desk = grid_T

        if flag2 == 1:
            if solve(sud_desk, 0, 0) == False:
                error = 1
            else:
                res = 1
            flag2 = 0
        if val != 0:
            draw_val(val)
            if valid(sud_desk, int(x), int(y), val) == True:
                if valid(sud_desk, int(x), int(y), val):
                    sud_desk[int(x)][int(y)] = val
                    flag1 = 0
                else:
                    sud_desk[int(x)][int(y)] = 0
                    raise_error2()
            val = 0

        if error == 1:
            raise_error1()
        if res == 1:
            result()
        draw()
        if flag1 == 1:
            change_cell()
        instruction_viz()

        pygame.display.update()


