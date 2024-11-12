import pygame
from src.game import start_level

levels = [
    [
        'S....',
        '.#.E.',
        '.....',
        '.F...'
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
	]
]

pygame.init()

for level in levels:
	completed = False
	while not completed:
		completed = start_level(level, tile_size=75)

pygame.quit()
