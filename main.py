import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 1200, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 28)

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, WHITE, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors

def draw_buttons():
    play_button = pygame.Rect(10, 10, 80, 40)
    pause_button = pygame.Rect(130, 10,  80, 40)
    clear_button = pygame.Rect(240, 10,  80, 40)
    
    pygame.draw.rect(screen, WHITE, play_button)
    pygame.draw.rect(screen, WHITE, pause_button)
    pygame.draw.rect(screen, WHITE, clear_button)

    play_text = font.render("Play", True, BLACK)
    pause_text = font.render("Pause", True, BLACK)
    clear_text = font.render("Clear", True, BLACK)

    screen.blit(play_text, (30, 20))
    screen.blit(pause_text, (140, 20))
    screen.blit(clear_text, (250, 20))
    
    return play_button, pause_button, clear_button

def main():
    running = True
    playing = False
    count = 0
    gen_count = 0
    update_freq = 60

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
            gen_count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        generation = gen_count // update_freq

        pygame.display.set_caption(f"Playing - Generation: {generation}" if playing else f"Paused - Generation: {generation}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                play_button, pause_button, clear_button = draw_buttons()
                
                if play_button.collidepoint((x, y)):
                    playing = True
                elif pause_button.collidepoint((x, y)):
                    playing = False
                elif clear_button.collidepoint((x, y)):
                    positions = set()
                    playing = False
                    count = 0
                    gen_count = 0
                else:
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)

                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    gen_count = 0
                
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)
    
        screen.fill(BLACK)
        draw_grid(positions)
        play_button, pause_button, clear_button = draw_buttons()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
