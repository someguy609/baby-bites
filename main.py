import pygame
from src.game import start_level

def show_menu(screen):
    start_menu = pygame.image.load("assets/start.png")
    quit_menu = pygame.image.load("assets/quit.png")
    
    start_menu = pygame.transform.scale(start_menu, (screen.get_width(), screen.get_height()))
    quit_menu = pygame.transform.scale(quit_menu, (screen.get_width(), screen.get_height()))
    
    menu_option = [quit_menu, start_menu]
    menu_state = True
    
    running = True
    
    while running:
        screen.fill((0,0,0))
        
        screen.blit(menu_option[menu_state], (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    menu_state = not menu_state
                
                elif event.key == pygame.K_RETURN:
                    if menu_state:
                        return
                    
                    if not menu_state:
                        pygame.quit()
                        exit()
        
        pygame.display.flip()


pygame.init()
tile_size = 100
screen = pygame.display.set_mode((1300, 950))


show_menu(screen)

levels = [
    [
        'S....',
        '.#.E.',
        '.....',
        '.F...',
    ],
    [
        '..S..',
        '.#.#.',
        'E#.#E',
        '.#.#.',
        '..F..',
    ],
    [
        '##########',
        '#S#...#FE#',
        '#...#.##.#',
        '###.#....#',
        '#.#.##.###',
        '#.#....#.#',
        '#...#.##.#',
        '#.###.#..#',
        '#...#...##',
        '##########',
    ],
    [
        'E........',
        '.###S###.',
        'E........',
        'F###.###.',
        'E........',
    ],
]

for level in levels:
    completed = False
    while not completed:
        completed = start_level(level, screen, tile_size)

pygame.quit()
