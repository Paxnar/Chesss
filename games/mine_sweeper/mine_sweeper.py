import sqlite3 as s3
import pygame
import os
import random
import sys
import itertools as it

def main(scr):
    global FONT_FOR_MINES, FONT_FOR_STATISTIC, DELTA_Y, DELTA_X, TILE_SIZE, MINES_COUNT, MINES_COLOR, GAMEMODE, difficulty, sprites, TILE_PICTURES, screen
    screen = scr
    FONT_FOR_MINES = pygame.font.Font(None, 110)  # Шрифл для количество оставшихся мин
    FONT_FOR_STATISTIC = pygame.font.Font(None, 55)  # Шрифт для количества побед и поражений игрока
    DELTA_Y = 30  # Сдвиг по оси Oy вниз, чтобы поле было по центру
    DELTA_X = 320  # Сдвиг по оси Ox вправо, чтобы поле было по центру
    TILE_SIZE = {(10, 10): 64, (16, 16): 40, (20, 20): 32}  # Размер для мины в зависимости от их количества
    MINES_COUNT = {(10, 10): 10, (16, 16): 35, (20, 20): 75}  # Кол-во мин в зависимости от размера поля
    MINES_COLOR = {1: (0, 162, 232), 2: (0, 140, 0), 3: (225, 255, 0), 4: (232, 174, 0),
                   5: (232, 40, 0), 6: (225, 0, 0), 7: (175, 245, 0), 8: (15, 9, 99)}
    # Цвета цифр в зависимости от того, сколько мир вокруг конкретной точки
    GAMEMODE = None
    # Словарь пар количество полей - обозначение
    difficulty = {(10, 10): "easy", (16, 16): "medium", (20, 20): "hard"}
    # Основная группа для всех спрайтов
    sprites = pygame.sprite.Group()

    TILE_PICTURES = {1: load_image(f"empty_tile.png"),
                     10: load_image("bomb.png"),
                     -1: load_image("closed_tile.png"),
                     11: load_image("touched_bomb.png"),
                     12: load_image("bomb_table.png"),
                     13: load_image("little_small_flag.png"),
                     15: load_image("button_1.png"),
                     14: load_image("untouched_mine.png"),
                     16: load_image("repeat_button.png"),
                     17: load_image("hint_button.png")}

    back = greeting_mine_sweeper()
    if back:
        return

    screen.fill((175, 170, 170))  # Закрашиваем экран

    # Отображение статистики перед началом, чтобы все были видны
    mine_sweeper.show_statisctic()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                destroy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mine_sweeper.click(*event.pos, pygame.mouse.get_pressed())
            if event.type == pygame.KEYDOWN:
                # Если нажата клавиша r - начинать игру заново
                if event.key in (pygame.K_r,):
                    mine_sweeper.restart()
                # Если нажата клавиша h - подсказку
                elif event.key == pygame.K_h:
                    mine_sweeper.hint()
                # Если нажата клавиша f - отображать все мины
                elif event.key in (pygame.K_f,):
                    mine_sweeper.show_left_red_mines()
                # Если нажата клавиша Esc - возвращаться в меню выбора сложности
                elif event.key == pygame.K_ESCAPE:
                    greeting_mine_sweeper()

        pygame.display.flip()
        sprites.draw(screen)
        mine_sweeper.render_screen()

def destroy() -> None:
    """Принудительный выход из игры"""
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Функция, которая загружает изображение для возможности использования его pygame'ом"""
    fullname = os.path.join('games\\mine_sweeper\\images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image





class Sprite(pygame.sprite.Sprite):
    def __init__(self, tile_key, x, y, size):
        super().__init__(sprites)
        self.image = pygame.transform.scale(TILE_PICTURES[tile_key], size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def greeting_mine_sweeper():

    """Функция, отображающая стартовую картинку"""
    global GAMEMODE
    global mine_sweeper
    background = pygame.transform.scale(load_image('MineSweeperScreen.png'), (1280, 720))
    screen.blit(background, (0, 0))
    # Создаем картинку-фон
    # Основной цикл показа картинки
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Если пользователь выходит из игры, тогда вызывать функцию destroy
                destroy()
            # Разные клавиши отвечают за разные режимы сложности
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    GAMEMODE = (10, 10)
                elif event.key == pygame.K_2:
                    GAMEMODE = (16, 16)
                elif event.key == pygame.K_3:
                    GAMEMODE = (20, 20)
                elif event.key == pygame.K_ESCAPE:
                    return True

                # Если клавиша или 1, или 2, или 3, то выбрасывать из функции
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    # Инициализация класса mine_sweeper для изменения сложности режима игры
                    mine_sweeper = MineSweeper(*GAMEMODE)
                    return False

        pygame.display.flip()


class MineSweeper:
    """Основной класс, реализующий весь функционал"""

    COUNT_WIN = 0
    GAME_OVER = False

    def __init__(self, width: int, height: int):
        self.cell_size = TILE_SIZE[(width, height)]
        self.height = height
        self.width = width
        self.field = self.generate_field(self.width, self.height, MINES_COUNT[(self.width, self.height)])
        self.flag_field = [[0] * self.width for _ in range(self.height)]  # Поля для отображенгия флагов
        self.mines_count = MINES_COUNT[(width, height)]  # Количество мин

        # Создание спрайтов неоткрытых клеточек
        for i in range(self.height):
            for j in range(self.width):
                Sprite(-1, DELTA_X + self.cell_size * j, DELTA_Y + self.cell_size * i, (self.cell_size,) * 2)

        # Отображение статистики
        self.show_statisctic()

    def render_screen(self) -> None:
        """Отрисовывать все клетки на поле"""
        for y in range(self.height):
            for x in range(self.width):
                if 1 <= self.field[y][x] <= 8:
                    f_ = pygame.font.Font(None, TILE_SIZE[(self.width, self.height)] + 3) # Шрифт для цифр
                    text = f_.render(f"{self.field[y][x]}", True, MINES_COLOR[self.field[y][x]])
                    x_coordinate = DELTA_X + self.cell_size * x  # Координата х для номера
                    y_coordinate = DELTA_Y + self.cell_size * y  # Координата y для номера
                    screen.blit(text, (x_coordinate, y_coordinate))

        # Отображаем количество оставшихся мин
        mines_remain = FONT_FOR_MINES.render(str(self.mines_count), True, (0, 0, 0))
        screen.blit(mines_remain, (1280 - 140, 484))

    def click(self, x_posit: int, y_posit: int, keys: list[int]) -> None:
        """В зависимости от положения мыши и нажатой кнопки запускает соответствующий алгоритм"""
        # Отображение всех оставшихся мин
        if 20 < x_posit < 300 and 387 < y_posit < 519:
            # Если игра не завершена
            if not self.GAME_OVER:
                self.show_left_red_mines()

        # Рестарт игры нажатием на кнопку
        if 20 < x_posit < 300 and 539 < y_posit < 673:
            # Рестарт игры
            self.restart()

        if 20 < x_posit < 300 and 235 < y_posit < 367:
            # Если егра еще не закончена
            if not self.GAME_OVER:
                # Выставление флажка
                self.hint()

        # если координата курсора вне поля
        if x_posit > DELTA_X + self.cell_size * len(self.field[0]) or x_posit < DELTA_X:
            return
        elif y_posit > DELTA_Y + self.cell_size * len(self.field) or y_posit < DELTA_Y:
            return

        x_ = (x_posit - DELTA_X) // self.cell_size  # Координата по оси Ox в self.field
        y_ = (y_posit - DELTA_Y) // self.cell_size  # Координата по оси Oy в self.field

        # Если нажата левая клавиша
        if keys[0]:
            self.open_cell(x_, y_)
        # Если нажата правая клавиша мыши
        elif keys[2]:
            self.set_flag(x_, y_)

    def set_flag(self, x: int, y: int) -> None:
        """Возможность установки флажка на месте предполагаемой мины"""
        if self.GAME_OVER:  # Если игра завершена
            return

        if self.field[y][x] in (-1, 10):  # Если это либо еще не открытая клетка, либо мина
            if self.flag_field[y][x] == 0:  # Если тут флага нет
                if not self.mines_count:  # Если и так бомб не осталось, выбрасываем
                    return
                self.make_sound("set_flag.mp3")  # Проигрывать звук

                self.flag_field[y][x] = 1  # Изменяем значение на 1 для отслеживания, где уже флаг стоит
                self.mines_count -= 1
                x_coordinate = DELTA_X + self.cell_size * x
                y_coordinate = DELTA_Y + self.cell_size * y
                # Заменяем спрайт
                Sprite(13, x_coordinate, y_coordinate, (self.cell_size,) * 2)

            elif self.flag_field[y][x] == 1:  # если тут флаг уже стоит
                self.make_sound("set_flag.mp3")  # Проигрывать звук

                self.flag_field[y][x] = 0  # Изменяем спрайт на 0, чтобы флага не было
                self.mines_count += 1
                x_coordinate = DELTA_X + self.cell_size * x
                y_coordinate = DELTA_Y + self.cell_size * y
                # Заменяем спрайт
                Sprite(-1, x_coordinate, y_coordinate, (self.cell_size,) * 2)

    def open_cell(self, x: int, y: int) -> None:
        """Функция, отвечающая за открытие клеток"""
        if self.GAME_OVER:  # Если переменная, отвечающая за проигрыш игрока, являетя True
            return

        if self.flag_field[y][x] == 1:  # Если на клетке соит флаг, открывать клетку не надо
            return

        # Проигрывать звук, если клетка не была открыта
        if self.field[y][x] in (-1, 10):
            self.make_sound("open_cell.mp3")  # Проигрывание звука нажатия

        if self.__is_mine(x, y):  # Если эта клеточка - мина
            x_coordinate = DELTA_X + x * self.cell_size
            y_coordinate = DELTA_Y + self.cell_size * y
            Sprite(11, x_coordinate, y_coordinate, (self.cell_size,) * 2)
            self.lose(x, y)  # Вызов функции отображения всех мин
            self.GAME_OVER = True

        elif not self.__is_mine(x, y):  # Если поле не мина
            if self.__mines_around(x, y) > 0:
                # Ставить цифру только в том случае, если рядом есть мин > 1,
                # a менять спрайт в любом случае
                self.field[y][x] = self.__mines_around(x, y)
            x_coordinate = DELTA_X + x * self.cell_size
            y_coordinate = DELTA_Y + y * self.cell_size
            Sprite(1, x_coordinate, y_coordinate, (self.cell_size,) * 2)

            # Увелчиваем количество оставшихся мин, если флаг был перекрыт
            if self.flag_field[y][x] == 1:
                self.flag_field[y][x] = 0
                self.mines_count += 1

        if not self.__mines_around(x, y):  # Раскрывать область только в том случае, если возле келтки вообще нет мин
            self.field[y][x] = 0  # Изменение самой клетки на 0, поскольку возле нее 0 мин
            for y_ in range(self.height):
                for x_ in range(self.width):
                    if self.__has_path((x, y), (x_, y_)) and self.field[y_][x_] != 10:
                        if self.flag_field[y_][x_] == 1:  # Увеличиваем кол-dо оставшихся мин
                            self.flag_field[y_][x_] = 0
                            self.mines_count += 1
                        # Проверка с помощью волнового алгоритма, касаются ли клетки, и, если да, нету ли там мины
                        self.field[y_][x_] = self.__mines_around(x_, y_)
                        x_coordinate = DELTA_X + x_ * self.cell_size  # Координата спрайта по оси Ox
                        y_coordinate = DELTA_Y + y_ * self.cell_size  # Координата спрайта по оси Oy
                        # Создание спрайта на месте координат
                        Sprite(1, x_coordinate, y_coordinate, (self.cell_size,) * 2)

                        # Открытие ячейки, которая возле мины
                        for w in range(-1, 2):
                            for h in range(-1, 2):
                                dx, dy = x_ + w, y_ + h  # Клетки вокруг x_, y_
                                if self.width > dx >= 0 and self.height > dy >= 0:  # Если они в пределах игрового поля
                                    x_coordinate = DELTA_X + self.cell_size * dx  # Координата по оси Ox
                                    y_coordinate = DELTA_Y + self.cell_size * dy  # Координата по оси Oy
                                    self.field[dy][dx] = self.__mines_around(dx, dy)
                                    Sprite(1, x_coordinate, y_coordinate, (self.cell_size,) * 2)

                                    # Увеличиваем кол-во оставшихся флагов
                                    if self.flag_field[dy][dx] == 1:
                                        self.flag_field[dy][dx] = 0
                                        self.mines_count += 1

        if self.win():
            self.make_sound("win.mp3")  # Проигрывать звук
            self.GAME_OVER = True
            self.show_final_mine(self.width, self.height)
            # Связь с бд
            with s3.connect("database.db") as connection:
                cur = connection.cursor()
                cur.execute(f"UPDATE rating SET wins = wins + 1 WHERE difficulty = '{difficulty[GAMEMODE]}'")

            # Отображение статистики
            self.show_statisctic()

    def win(self) -> bool:
        """Каждый раз проверяет, победил ли игрок"""
        opened_cells_count = 0

        # Цикл обхода всех клеток
        for i in range(self.width):
            for j in range(self.height):
                if 0 <= self.field[j][i] <= 8:
                    opened_cells_count += 1

        # Сравнение общего количества открытых клеток с количеством всех пустых клеток
        return opened_cells_count == (self.height * self.width - MINES_COUNT[(self.width, self.height)])

    def lose(self, f_x: int, f_y: int) -> None:
        """Функция, завершающая игру при нажатии на мину.
           f_x, f_y - координаты мины, на которую нажали, и которую не надо перекрашиватьв цвет обычной клетки-мины"""

        self.make_sound("kaboom.mp3")  # Проигрывать звук

        for x in range(self.width):
            for y in range(self.height):
                if self.__is_mine(x, y):
                    if f_y == y and f_x == x:
                        continue  # При совпадении пропускать этот цикл
                    x_coordinate = DELTA_X + self.cell_size * x  # Коодрината по оси Ox
                    y_coordinate = DELTA_Y + y * self.cell_size  # Коодрината по оси Oy
                    Sprite(10, x_coordinate, y_coordinate, (self.cell_size,) * 2)

        # Соединение с базой данных
        with s3.connect('games/mine_sweeper/database.db') as con:
            cur = con.cursor()
            cur.execute(f"UPDATE rating SET loses = loses + 1 WHERE difficulty = '{difficulty[GAMEMODE]}'")

        # Отображение статистики игрока
        self.show_statisctic()

    def restart(self) -> None:
        """Начинает игру заново"""
        # Очистка всех ранее добавленных спрайтов
        sprites.empty()

        # Обнуление переменной-флага, отвечающей за окончание игры
        self.GAME_OVER = False

        # Генерация полей и счетчика мин по новой
        self.field = self.generate_field(self.width, self.height, MINES_COUNT[(self.width, self.height)])
        self.flag_field = [[0] * self.width for _ in range(self.height)]  # Поля для отображенгия флагов
        self.mines_count = MINES_COUNT[(self.width, self.height)]  # Количество мин

        # Создание спрайтов
        for i in range(self.height):
            for j in range(self.width):
                Sprite(-1, DELTA_X + self.cell_size * j, DELTA_Y + self.cell_size * i, (self.cell_size,) * 2)

    def show_left_red_mines(self) -> None:
        """Отображение всех мин красным цветом и завершение игры"""
        self.GAME_OVER = True

        # Проигрывание звука взрыва бомбы
        self.make_sound("kaboom.mp3")

        # Отображение мин в зависимости от положения в списке поля
        for y in range(self.height):
            for x in range(self.width):
                if 9 < self.field[y][x] < 11:
                    Sprite(11, DELTA_X + x * self.cell_size, DELTA_Y + self.cell_size * y, (self.cell_size,) * 2)

    def show_statisctic(self) -> None:
        """Отображение статистики побед/поражений игрока"""
        with s3.connect("games/mine_sweeper/database.db") as connection:
            cur = connection.cursor()
            # Количество побед и смертей, полученные из бд
            win, death = cur.execute(f"SELECT wins, loses FROM rating WHERE difficulty = "
                                     f"'{difficulty[GAMEMODE]}'").fetchone()

        # Очистка экрана для стирания ранее существовавшей надписи, чтобы они друг друга не перекрывали
        screen.fill((175, 175, 175))

        # Кнопка подсказки
        Sprite(17, 20, 235, (280, int(280 / 2.12)))

        # Создание счетчика оставшихся бомб
        Sprite(12, 1280 - 300, 450, (280, int(280 / 2.12)))

        # Создание кнопки отображения всех мин
        Sprite(15, 20, 387, (280, int(280 / 2.12)))

        # Создание кнопки переигрывания
        Sprite(16, 20, 539, (280, int(280 / 2.12)))

        # Создание тексовых надписей
        self.count_death = FONT_FOR_STATISTIC.render(f'Total deaths: {death}', True, (250, 1, 1))
        self.count_win = FONT_FOR_STATISTIC.render(f'Total wins: {win}', True, (2, 250, 2))
        self.k_d = FONT_FOR_STATISTIC.render(f'Your k/d {round(win / death, 2)}', True, (5, 215, 215))
        screen.blit(self.count_death, (5, 105))
        screen.blit(self.count_win, (5, 44))
        screen.blit(self.k_d, (5, 166))

    def hint(self) -> None:
        """Дать подсказку игроку"""

        all_mines = []  # Все мины

        #  Тривиальный перебор всех индексов в поле для нахождения тех, где стоят мины
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == 10:
                    all_mines.append((x, y))

        # Фильтрация тех пар координат, где уже есть флаг
        # (их удаление, чтобы подсказка не была истрачена впустую и не был установлен флаг)
        all_mines = tuple(it.filterfalse(lambda x: self.flag_field[x[1]][x[0]] == 1, all_mines))

        # Если свободных от флажков клеток больше не осталось - выбрасывать прочь из функциии
        if not all_mines:
            return

        # Сама установка флага
        self.set_flag(*random.choice(all_mines))

    def show_final_mine(self, w: int, h: int) -> None:
        """Отображаем зеленым цветом мины, которые остались"""
        for x in range(w):
            for y in range(h):
                if self.field[y][x] == 10:
                    Sprite(14, DELTA_X + x * self.cell_size, DELTA_Y + y * self.cell_size, (self.cell_size,) * 2)

    def __has_path(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        """Возваращет True либо False в зависимости от того, возможно ли пройти от координаты start до end"""
        MAX = 10 ** 5  # Какое-то условное очень большое число
        x, y = start  # Берем координаты стартовой позиции

        # Массив, аналогичный self.field, заполненный этими большими значениями
        distance = [[MAX] * self.width for _ in range(self.height)]

        # Значение массива с индексами x и y приравниваем к 0
        distance[y][x] = 0

        # Массив, который будет содержать предыдущее состояние, заполняем None (такие же размеры)
        previous = [[None] * self.width for _ in range(self.height)]

        # Динамически генерирующаяся очередь
        queue = [(x, y)]

        while queue:
            # Пока она не пуста, переменным x и y даем значения первого индекса очереди, при этом удаляя его из нее.
            x, y = queue.pop(0)
            for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                # Потом обходим те значения, которые отличаются от x и y максимум на единицу (НЕ по диаг.)
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height \
                        and not self.__mines_around(next_x, next_y) and distance[next_y][next_x] == MAX:
                    # Если ничего не выходит за пределы, и значение [x + dx][y + dy] - MAX,
                    # главный массив с этими координатами увеличиваем на единицу относительно [x][y],
                    distance[next_y][next_x] = distance[y][x] + 1
                    # а массив, содержвщий прежнее состояние, по индексу х + dx и y + dy становится равен x и y
                    previous[next_y][next_x] = x, y
                    queue.append((next_x, next_y))

        x, y = end

        # Возвращаем инвертированное булевое значение в зависимости то того, если start равен end, или
        # массив по индексу [x][y] равен тому значению по умолчанию
        return not (distance[y][x] == MAX or start == end)

    def __mines_around(self, x: int, y: int) -> int:
        """Возвращает количество мин вокруг"""
        count = 0
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                if not any((x + delta_x < 0, x + delta_x >= self.width, delta_y + y >= self.height, delta_y + y < 0)):
                    if self.field[delta_y + y][delta_x + x] == 10:
                        count += 1
        return count

    def __is_mine(self, x: int, y: int) -> bool:
        """Проверка того, что клеточка - мина"""
        return self.field[y][x] == 10

    @staticmethod
    def generate_field(w: int, h: int, mine_count: int) -> list[list]:
        """Генерирует поле"""
        field = [[-1] * w for _ in range(h)]  # Поле
        for _ in range(mine_count):
            x, y = random.randrange(0, w), random.randrange(0, h)  # Координаты мины
            while field[y][x] == 10:  # Если на этих кордах мина уже стоит,
                x, y = random.randrange(0, w), random.randrange(0, h)  # перегенеринровать
            field[y][x] = 10

        # Возвращение самого поля
        return field

    @staticmethod
    def make_sound(s: str) -> None:
        """Проигрывать звуки"""
        soun = pygame.mixer.Sound(os.path.join("games/mine_sweeper/sounds", f"{s}"))
        pygame.mixer.Sound.play(soun)
        pygame.mixer.music.stop()



