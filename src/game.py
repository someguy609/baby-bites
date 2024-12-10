import random
import pygame
from .entities import Player, Enemy, Wall, Food

def start_level(level: list[str], screen, tile_size=50) -> bool:

    width = len(level[0])
    height = len(level)
    
    screen_width, screen_height = screen.get_size()
    
    x_offset = (screen_width - width*tile_size) // 2
    y_offset = (screen_height - height*tile_size) // 2

    player = None
    enemies = []
    walls = []
    finish = None
    food = None

    # wall = 

    floor = pygame.image.load('assets/floor.png')
    floor = pygame.transform.scale(floor, (tile_size, tile_size))

    for i in range(len(level)):
        for j in range(len(level[i])):
            match level[i][j]:
                case 'S':
                    player = Player(level, (j, i), tile_size)
                case 'E':
                    enemies.append(Enemy(level, (j, i), tile_size, 2))
                case '#':
                    walls.append(Wall((j, i), tile_size, x_offset, y_offset))
                case 'F':
                    food = Food((j, i), tile_size, x_offset, y_offset)
                    finish = (j, i)

    # screen = pygame.display.set_mode((width * tile_size, height * tile_size))
    playing = True

    while playing:
        screen.fill((0, 0, 0))
        for i in range(height):
            for j in range(width):
                screen.blit(floor, (j * tile_size + x_offset, i * tile_size + y_offset))
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return 'quit', None
            player.update()
        player.draw(screen, x_offset, y_offset)
        if (player.x, player.y) == finish:
            break
        Enemy.traffic = [[0 for _ in level[0]] for _ in level]
        for enemy in enemies:
            if (player.x, player.y) == (enemy.x, enemy.y):
                return 'reset', None
            if player.moved:
                enemy.update((player.x, player.y),algo=random.sample(['a_star', 'alpha_beta'], 1)[0])
            enemy.draw(screen, x_offset, y_offset)
        player.moved = False
        for wall in walls:
            wall.draw(screen)
        if food:
            food.draw(screen)
        pygame.display.flip()
        pygame.display.update()
    
    return 'completed', player.moves
