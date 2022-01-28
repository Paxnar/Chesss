import os
import time

import pygame
import sys


def load_level(filename):
    filename = 'levels\\' + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def load_image(name, color_key=None):
    fullname = os.path.join('images\\', name)
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


def check_move(sprite, group):
    return pygame.sprite.spritecollideany(sprite, group)



class Grnd(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(grnd_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, act=False):
        super().__init__(boxes_group, all_sprites)
        self.act = act
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_images["pl1"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Env(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(env_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    env = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Grnd('ground', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '@':
                Grnd('ground', x, y)
                new_player = Player(x, y)
            elif level[y][x] == "b":
                Grnd('ground', x, y)
                Box('box', x, y)
            elif level[y][x] == "e":
                Env('env', x, y)
                env += 1
            elif level[y][x] == "c":
                Env('env', x, y)
                Box('box1', x, y, True)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, env


def main(scr, lvl=6):
    global screen, tile_width, player, boxes, all_sprites, boxes_group, env_group, grnd_group, walls_group, player_group, tile_width, tile_height, tile_images, player_images
    tile_width = tile_height = 64
    player = None
    boxes = []
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    grnd_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    boxes_group = pygame.sprite.Group()
    env_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('sprites\\block.png'),
        'ground': load_image('sprites\\ground.png'),
        'box': load_image('sprites\\crate.png'),
        'box1': load_image('sprites\\crate_1.png'),
        'env': load_image('sprites\\env.png')
    }
    player_images = {
        'pl1': load_image('sprites\\player_01.png', -1),
        'pl2': load_image('sprites\\player_02.png', -1),
        'pl3': load_image('sprites\\player_03.png', -1),
        'pl4': load_image('sprites\\player_04.png', -1)
    }
    screen = scr
    pygame.display.set_caption("PyGames")
    player, level_x, level_y, env = generate_level(load_level(f"lvl{lvl}.txt"))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.image = player_images["pl4"]
                    player.rect.x -= 64
                    box = check_move(player, boxes_group)
                    if check_move(player, walls_group):
                        player.rect.x += 64
                    elif box:
                        box.rect.x -= 64
                        if box.act:
                            box.act = False
                            box.image = tile_images['box']
                            env += 1
                        if check_move(box, walls_group) or (check_move(box, boxes_group) and check_move(box, boxes_group) != box):
                            player.rect.x += 64
                            box.rect.x += 64
                        if check_move(box, env_group):
                            box.act = True
                            box.image = tile_images['box1']
                            env -= 1

                if event.key == pygame.K_RIGHT:
                    player.image = player_images["pl3"]
                    player.rect.x += 64
                    box = check_move(player, boxes_group)
                    if check_move(player, walls_group):
                        player.rect.x -= 64
                    elif box:
                        box.rect.x += 64
                        if box.act:
                            box.act = False
                            box.image = tile_images['box']
                            env += 1
                        if check_move(box, walls_group) or (check_move(box, boxes_group) and check_move(box, boxes_group) != box):
                            player.rect.x -= 64
                            box.rect.x -= 64
                        if check_move(box, env_group):
                            box.act = True
                            box.image = tile_images['box1']
                            env -= 1

                if event.key == pygame.K_UP:
                    player.image = player_images["pl2"]
                    player.rect.y -= 64
                    box = check_move(player, boxes_group)
                    if check_move(player, walls_group):
                        player.rect.y += 64
                    elif box:
                        box.rect.y -= 64
                        if box.act:
                            box.act = False
                            box.image = tile_images['box']
                            env += 1
                        if check_move(box, walls_group) or (check_move(box, boxes_group) and check_move(box, boxes_group) != box):
                            player.rect.y += 64
                            box.rect.y += 64
                        if check_move(box, env_group):
                            box.act = True
                            box.image = tile_images['box1']
                            env -= 1

                if event.key == pygame.K_DOWN:
                    player.image = player_images["pl1"]
                    player.rect.y += 64
                    box = check_move(player, boxes_group)
                    if check_move(player, walls_group):
                        player.rect.y -= 64
                    elif box:
                        box.rect.y += 64
                        if box.act:
                            box.act = False
                            box.image = tile_images['box']
                            env += 1
                        if check_move(box, walls_group) or (check_move(box, boxes_group) and check_move(box, boxes_group) != box):
                            player.rect.y -= 64
                            box.rect.y -= 64
                        if check_move(box, env_group):
                            box.act = True
                            box.image = tile_images['box1']
                            env -= 1
                if event.key == pygame.K_c:
                    main(screen, lvl)
        screen.fill((0, 0, 0))
        walls_group.draw(screen)
        grnd_group.draw(screen)
        env_group.draw(screen)
        boxes_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        if env == 0:
            time.sleep(1)
            main(screen, lvl + 1)
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    size = width, height = 64 * 8, 64 * 8
    screen = pygame.display.set_mode(size)
    main(screen)
