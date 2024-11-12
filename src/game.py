import pygame
from .entities import Player, Enemy, Wall

def start_level(level: list[str], tile_size=50) -> bool:

    width = len(level[0])
    height = len(level)

    player = None
    enemies = []
    walls = []
    finish = None

    for i in range(len(level)):
        for j in range(len(level[i])):
            match level[i][j]:
                case 'S':
                    player = Player(level, (j, i), tile_size)
                case 'E':
                    enemies.append(Enemy(level, (j, i), tile_size))
                case '#':
                    walls.append(Wall((j, i), tile_size))
                case 'F':
                    finish = (j, i)

    screen = pygame.display.set_mode((width * tile_size, height * tile_size))
    playing = True

    while playing:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return False
            player.update()
        player.draw(screen)
        if (player.x, player.y) == finish:
            break
        if player.moved:
            for enemy in enemies:
                enemy.update((player.x, player.y))
            player.moved = False
        for enemy in enemies:
            if (player.x, player.y) == (enemy.x, enemy.y):
                break
            enemy.draw(screen)
        for wall in walls:
            wall.draw(screen)
        pygame.display.flip()
        pygame.display.update()
    
    return True
