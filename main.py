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
        
def show_finished_screen(screen, high_score):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    
    text = font.render("All Levels Complete!", True, (255, 255, 255))
    score_text = small_font.render(f"Moves Taken: {high_score}", True, (255, 255, 255))
    replay_text = small_font.render("Press R to Play Again", True, (255, 255, 255))
    quit_text = small_font.render("Press Q to Quit", True, (255, 255, 255))
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 150))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 250))
        screen.blit(replay_text, (screen.get_width() // 2 - replay_text.get_width() // 2, 350))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 450))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Replay
                elif event.key == pygame.K_q:
                    return False  # Quit
        
        pygame.display.flip()


pygame.init()
tile_size = 100
screen = pygame.display.set_mode((1300, 950))

high_score = float('inf')
player_moves = 0

show_menu(screen)

levels = [
    [
        'S....',
        '.##E.',
        '..#..',
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
        '#.#....#E#',
        '#...#.##.#',
        '#.###.#..#',
        '#..E#...##',
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

while True:

    state = None

    for level in levels:

        if state == 'quit':
            break

        state = 'reset'

        while state == 'reset':
            state, moves = start_level(level, screen, tile_size)
        
        match state:
            case 'completed':
                player_moves += moves
            case 'quit':
                break
            # if completed:
            #     player_moves += moves
                # print("Player moves: {player_moves} Moves: {moves}")
    
    if state == 'quit':
        break

    high_score = min(high_score, player_moves)
        
    replay = show_finished_screen(screen, high_score)

    if not replay:
        break


pygame.quit()
