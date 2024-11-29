import pygame
from .entities import Player, Enemy, Wall

def start_level(level: list[str], screen, tile_size=50) -> bool:

    width = len(level[0])
    height = len(level)
    
    screen_width, screen_height = screen.get_size()
    
    x_offset = (screen_width - width*tile_size) // 2
    y_offset = (screen_height - height*tile_size) // 2
    
    print(x_offset)
    print(width)

    player = None
    enemies = []
    walls = []
    finish = None

    # wall = 

    floor = pygame.image.load('assets/floor.png')
    floor = pygame.transform.scale(floor, (tile_size, tile_size))

    for i in range(len(level)):
        for j in range(len(level[i])):
            match level[i][j]:
                case 'S':
                    player = Player(level, (j, i), tile_size)
                case 'E':
                    enemies.append(Enemy(level, (j, i), tile_size))
                case '#':
                    walls.append(Wall((j, i), tile_size, x_offset, y_offset))
                case 'F':
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
                    return False
            player.update()
        player.draw(screen, x_offset, y_offset)
        if (player.x, player.y) == finish:
            break
        if player.moved:
            for enemy in enemies:
                enemy.update((player.x, player.y))
            player.moved = False
        for enemy in enemies:
            if (player.x, player.y) == (enemy.x, enemy.y):
                break
            enemy.draw(screen, x_offset, y_offset)
        for wall in walls:
            wall.draw(screen)
        pygame.display.flip()
        pygame.display.update()
    
    return True
