import pygame
from typing import List, Tuple

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 70  # Extra space for the button
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
DELAY_TIME = 330  # Milliseconds


# Functions to handle the grid drawing and cell updates:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_cells(grid: List[List[int]]):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = GREEN if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_cell_position(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    x, y = mouse_pos
    return y // CELL_SIZE, x // CELL_SIZE


# game_of_life functions:
def evaluate_NN(cell, N1, N2, N3, N4, N5, N6, N7, N8):
    N_sum = N1 + N2 + N3 + N4 + N5 + N6 + N7 + N8
    if N_sum == 3:
        return 1
    elif N_sum ==2 and cell == 1:
        return 1
    else:
        return 0

def game_of_life(grid: List[List[int]]) -> List[List[int]]:
    """
        Use repeating boundary conditions.

        - If alive with 0,1 or 4 NN then dies
        - If alive with 2,3 NN then lives
        - New life from dead if exactly 3 NN are alive
    """
    N_rows = len(grid)
    N_columns = len(grid[0])

    for r in grid[1:]:
        assert N_columns == len(r), "Ensure all columns have the same length!"

    next_generation = []
    
    for i in range(N_rows):
        next_generation.append([])
        for j in range(N_columns):
            next_r = i + 1
            next_c = j + 1
            if next_r >= N_rows:
                next_r = 0
            if next_c >= N_columns:
                next_c = 0
            #pdb.set_trace()
            next_generation[i].append(
                evaluate_NN(
                    grid[i][j],
                    grid[i-1][j], # left
                    grid[i][j-1], # up
                    grid[next_r][j], # right
                    grid[i][next_c], # down
                    grid[i-1][j-1], # up-left
                    grid[next_r][j-1], # up-right
                    grid[next_r][next_c], # down-right
                    grid[i-1][next_c], # down-left
                )
            )

    return next_generation

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.text, 1, BLACK)
        screen.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


def main():
    generation_count = 0
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    running = True
    simulation_running = False
    draw_grid_bool = False

    start_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 50, 'Start', GREEN, (0, 255, 0))
    reset_button = Button(SCREEN_WIDTH - 150, 10, 120, 50, 'Reset', GREEN, (0, 255, 0))
    grid_button = Button(SCREEN_WIDTH - 300, 10, 120, 50, 'Grid', GREEN, (0, 255, 0))


    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not simulation_running and start_button.is_over(pos):
                    simulation_running = True
                    start_button.text = "Pause"
                elif simulation_running and start_button.is_over(pos):
                    simulation_running = False
                    start_button.text = "Start"
                elif not simulation_running:
                    row, col = get_cell_position(event.pos)
                    grid[row][col] = 1 if grid[row][col] == 0 else 0

        if reset_button.is_over(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            simulation_running = False
            start_button.text = "Start"
            generation_count = 0

        if grid_button.is_over(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_grid_bool:
                draw_grid_bool = False
            elif not draw_grid_bool:
                draw_grid_bool = True

        if simulation_running:
            pygame.time.wait(DELAY_TIME)
            grid = game_of_life(grid)
            generation_count += 1

            # Display the generation count
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(f"Generation: {generation_count}", 1, WHITE)
            screen.blit(text, (10, SCREEN_HEIGHT - 40))

        draw_cells(grid)
        if draw_grid_bool:
            draw_grid()
        start_button.draw(screen, outline=WHITE)
        reset_button.draw(screen, outline=WHITE)
        grid_button.draw(screen, outline=WHITE)

        pygame.display.flip()

    pygame.quit()

# Run the game
main()

