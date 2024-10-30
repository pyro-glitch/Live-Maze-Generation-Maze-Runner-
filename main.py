import time
import random
from threading import Thread
import pygame
from Clock import Clock

# Config Constants
DIM_X = 20 # map size
DIM_Y = 20  

NEW_SPRITE_SIZE = 32 # change as per above values
PLAYER_RADIUS = 8 

CHANGE_TIME = 5 # time between map change
MAP_STEPS = 300 # defines how much the map should change

# Do not change unless u know what you'r doing
SPRITE_SIZE = 16
NUM_SPRITES = 15
MAX_INDEX = DIM_X - 1
DIRECTIONS = ["v", ">", "^", "<"]
start_x = DIM_X - 1
start_y = DIM_Y - 1
PLAYER_X = DIM_X - 1
PLAYER_Y = DIM_Y - 1
PLAYER_COLOR = (0, 0, 255)
PLAYER_STEPS = 0
TEXT_COLOR = (0, 0, 0)
OFFSET = [30, 30]
clock = Clock()
gameState = 1  # 1-started, 2-running, 3-won
instructions = ["Press To Start", "Go To The", " You Won!", "Arrow Keys", "Red dot", ""]

# Load and process sprite sheet
sprite_sheet = pygame.image.load('maze-sprite-4.png')
sprites = [
    pygame.transform.scale(
        sprite_sheet.subsurface((i * SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE)),
        (NEW_SPRITE_SIZE, NEW_SPRITE_SIZE)
    )
    for i in range(NUM_SPRITES)
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))

# Font for rendering text
font = pygame.font.Font(None, 48)  # Choose font size 74 for the title
pygame.display.set_caption("Maze Runner")

# Maze parameters
s_val = [
    "1000", "0100", "0010", "0001",
    "0011", "1001", "0110", "1100",
    "0111", "1011", "1101", "1110",
    "0101", "1010", "1111"
]

# Initialize maze grid
m = []
row1 = [">"] * (DIM_X - 1) + ["v"]
row2 = ["v"] + ["<"] * (DIM_X - 1)
for i in range(DIM_Y-1):
    if i % 2==0:
        m.append(list(row1))
    else:
        m.append(list(row2))

row1[DIM_X - 1] = "*"
m.append(list(row1))


def get_sprite(i, j):
    u = d = l = r = 0

    # Left
    if i > 0 and m[j][i - 1] == ">": l = 1

    # Right
    if i < MAX_INDEX and m[j][i + 1] == "<": r = 1

    # Up
    if j > 0 and m[j - 1][i] == "v": u = 1

    # Down
    if j < MAX_INDEX and m[j + 1][i] == "^": d = 1

    # Self
    temp = m[j][i]
    if temp == "<":
        l = 1
    elif temp == "^":
        u = 1
    elif temp == ">":
        r = 1
    elif temp == "v":
        d = 1

    sprite_key = f"{l}{u}{r}{d}"
    return sprites[s_val.index(sprite_key)]


def update_map(start_x, start_y):
    t_dir = list(DIRECTIONS)

    if start_x == 0: t_dir.remove("<")
    if start_x == MAX_INDEX: t_dir.remove(">")
    if start_y == 0: t_dir.remove("^")
    if start_y == MAX_INDEX: t_dir.remove("v")

    new_dir = random.choice(t_dir)
    m[start_y][start_x] = new_dir

    if new_dir == ">":
        start_x += 1
    elif new_dir == "<":
        start_x -= 1
    elif new_dir == "v":
        start_y += 1
    elif new_dir == "^":
        start_y -= 1

    m[start_y][start_x] = "*"
    return start_x, start_y


def generate_map():
    global start_x, start_y
    while True:
        if gameState == 2:
            for _ in range(MAP_STEPS):
                start_x, start_y = update_map(start_x, start_y)
            time.sleep(CHANGE_TIME)


def handle_player_movement(player_x, player_y, steps):
    global gameState
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, None, False

        if event.type == pygame.KEYDOWN:
            if gameState == 1 and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                clock.start()
                gameState = 2

            if event.key == pygame.K_UP and player_y > 0:
                if m[player_y][player_x] == '^' or m[player_y - 1][player_x] == 'v':
                    player_y -= 1
                    steps = steps + 1

            elif event.key == pygame.K_DOWN and player_y < MAX_INDEX:
                if m[player_y][player_x] == 'v' or m[player_y + 1][player_x] == '^':
                    player_y += 1
                    steps = steps + 1

            elif event.key == pygame.K_LEFT and player_x > 0:
                if m[player_y][player_x] == '<' or m[player_y][player_x - 1] == '>':
                    player_x -= 1
                    steps = steps + 1

            elif event.key == pygame.K_RIGHT and player_x < MAX_INDEX:
                if m[player_y][player_x] == '>' or m[player_y][player_x + 1] == '<':
                    player_x += 1
                    steps = steps + 1

            elif event.key == pygame.K_ESCAPE:
                return player_x, player_y, False

    return player_x, player_y, True, steps


# Start the map generation thread
map_thread = Thread(target=generate_map)
map_thread.daemon = True
map_thread.start()

# Main loop
running = True
while running:
    PLAYER_X, PLAYER_Y, running, PLAYER_STEPS = handle_player_movement(PLAYER_X, PLAYER_Y, PLAYER_STEPS)
    if not running:
        break

    if PLAYER_X == 0 and PLAYER_Y == 0:
        gameState = 3
        clock.stop()
        # print("PLAYER WON")

    # Draw maze
    screen.fill((255, 255, 255))
    for j in range(DIM_X):
        for i in range(DIM_Y):
            sprite = get_sprite(i, j)
            screen.blit(sprite, (i * NEW_SPRITE_SIZE + OFFSET[0], j * NEW_SPRITE_SIZE + OFFSET[1]))
    
  # Draw Goal
    pygame.draw.circle(
        screen, (255, 0, 0),
        (NEW_SPRITE_SIZE // 2 + OFFSET[0],
         NEW_SPRITE_SIZE // 2 + OFFSET[1]),
        PLAYER_RADIUS
    )

    # Draw Player
    pygame.draw.circle(
        screen, PLAYER_COLOR,
        (PLAYER_X * NEW_SPRITE_SIZE + NEW_SPRITE_SIZE // 2 + OFFSET[0],
         PLAYER_Y * NEW_SPRITE_SIZE + NEW_SPRITE_SIZE // 2 + OFFSET[1]),
        PLAYER_RADIUS
    )

    # Draw UI
    steps_label_surface = font.render("Steps:", True, TEXT_COLOR)
    steps_value_surface = font.render(str(PLAYER_STEPS), True, TEXT_COLOR)
    time_label_surface = font.render("Time:", True, TEXT_COLOR)
    time_value_surface = font.render(str(round(clock.get_time(), 2)), True, TEXT_COLOR)
    text_surface = font.render(instructions[gameState - 1], True, TEXT_COLOR)
    text_surface2 = font.render(instructions[gameState + 2], True, TEXT_COLOR)

    screen.blit(steps_label_surface, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 2))
    screen.blit(steps_value_surface, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 3))
    screen.blit(time_label_surface, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 4))
    screen.blit(time_value_surface, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 5))
    screen.blit(text_surface, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 8))
    screen.blit(text_surface2, (DIM_Y * NEW_SPRITE_SIZE + 5 + OFFSET[0], 50 * 9))

    pygame.display.flip()
    time.sleep(0.1)  # Adjust the sleep time for smoother gameplay

pygame.quit()
