from typing import Tuple, List, Any

import pygame
import random


# Game state
def generate():
    return [[random.choice([True, False]) for j in range(grid_size[1])] for i in range(grid_size[0])]


# Game rules
def update_grid(grid):
    for row in range(grid_size[0]):
        for column in range(grid_size[1]):
            if grid[row][column]:
                if neighbors_alive[(row, column)] < 2:
                    grid[row][column] = False
                elif neighbors_alive[(row, column)] > 3:
                    grid[row][column] = False
            else:
                if neighbors_alive[(row, column)] == 3:
                    grid[row][column] = True
    return grid


# Mapping of neighboring grid
def neighbors_map(rows, cols):
    neighbors = {(i, j): [(x % rows, y % cols) for x in range(i - 1, i + 2)
                          for y in range(j - 1, j + 2)] for i in range(rows)
                 for j in range(cols)}
    # Remove the central cell from the list of neighbours
    for key, value in neighbors.items():
        value.remove(key)
    return neighbors


# Counting alive neighbors
def count_neighbors(grid):
    for pos, neighbors in neighbors_map.items():
        count = 0
        for x, y in neighbors:
            if grid[x][y]:
                count += 1
        neighbors_alive[pos] = count


# Draw the grid
def draw(grid):
    for row in range(grid_size[0]):
        for column in range(grid_size[1]):
            # Calculate the coordinates of the cell's top-left corner
            x = column * cell_size
            y = row * cell_size
            color = (0, 0, 0)
            if grid[row][column]:
                color = (255, 255, 255)
            # Draw the cell as a rectangle
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size), 1)


# Define grid size and cell size
grid_size: tuple[int, int] = (60, 60)    # number of rows and columns in the grid
cell_size: int = 10                      # size of each cell in pixels

# Calculate the total size of the grid in pixels
grid_width: int = grid_size[0] * cell_size
grid_height: int = grid_size[1] * cell_size

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((grid_width, grid_height))

# Create a clock object to limit the frame rate
clock = pygame.time.Clock()

# Generate the first state
grid: list[list[Any]] = generate()

# Create a dictionary to store the neighbors of each cell
neighbors_map = neighbors_map(grid_size[0], grid_size[1])

# Create dictionary for keeping alive counts and populate it
neighbors_alive = {}
count_neighbors(grid)

# Set the maximum frames per second
max_fps = 10

running = True
while running:

    time_since_last_update = clock.tick(max_fps)
    if time_since_last_update >= 1000 / max_fps:
        # Update the game view
        draw(grid)
        pygame.display.update()

        # Prepare the next state
        count_neighbors(grid)
        grid = update_grid(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid = generate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

# Clean up Pygame resources
pygame.quit()
