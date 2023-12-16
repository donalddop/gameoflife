import pygame
import random


class Grid:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.neighbors_map = self.create_neighbors_map()
        self.neighbors_alive = {}
        self.grid = []
        self.generate_grid()
        self.count_alive_neighbors()

    # Counting alive neighbors
    def count_neighbors(self):
        for pos, neighbors in self.neighbors_map.items():
            count = 0
            for x, y in neighbors:
                if self.grid[x][y]:
                    count += 1
            self.neighbors_alive[pos] = count

    def generate_grid(self):
        self.grid = [[random.choice([True, False]) for j in range(self.grid_size[1])] for i in range(self.grid_size[0])]

    # Game rules
    def update_grid(self):
        for row in range(self.grid_size[0]):
            for column in range(self.grid_size[1]):
                if self.grid[row][column]:
                    if self.neighbors_alive[(row, column)] < 2:
                        self.grid[row][column] = False
                    elif self.neighbors_alive[(row, column)] > 3:
                        self.grid[row][column] = False
                else:
                    if self.neighbors_alive[(row, column)] == 3:
                        self.grid[row][column] = True

    # Mapping of neighboring grid
    def create_neighbors_map(self):
        neighbors = {(i, j): [(x % self.grid_size[0], y % self.grid_size[1]) for x in range(i - 1, i + 2)
                              for y in range(j - 1, j + 2)] for i in range(self.grid_size[0])
                     for j in range(self.grid_size[1])}
        # Remove the central cell from the list of neighbours
        for key, value in neighbors.items():
            value.remove(key)
        return neighbors

    # Counting alive neighbors
    def count_alive_neighbors(self):
        for pos, neighbors in self.neighbors_map.items():
            count = 0
            for x, y in neighbors:
                if self.grid[x][y]:
                    count += 1
            self.neighbors_alive[pos] = count


class GameApp:
    def __init__(self, grid):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.max_fps = 144
        self.screen = pygame.display.set_mode((grid.grid_size[1] * grid.cell_size, grid.grid_size[0] * grid.cell_size),
                                              pygame.RESIZABLE)
        self.running = True
        self.pause = False
        self.leftMouse_down = False

    # Draw the grid
    def draw(self, grid):
        for row in range(grid.grid_size[0]):
            for column in range(grid.grid_size[1]):
                # Calculate the coordinates of the cell's top-left corner
                x = column * grid.cell_size
                y = row * grid.cell_size
                color = (0, 0, 0)
                # Color cell if it is alive
                if grid.grid[row][column]:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # Draw the cell as a rectangle
                pygame.draw.rect(self.screen, color, (x, y, grid.cell_size, grid.cell_size), 1)
        pygame.display.update()

    # Function to toggle a cell
    def toggle_cell(self, grid):
        # Get the position of the mouse click
        mouse_pos = pygame.mouse.get_pos()
        # Check which grid space the mouse is over
        if mouse_pos is not None:
            x = mouse_pos[0] // grid.cell_size
            y = mouse_pos[1] // grid.cell_size

            # Toggle the state of the cell
            grid.grid[y][x] = 1
            self.draw(grid)

    def game_loop(self, grid):
        while self.running:

            # Limit the frame rate
            if not self.pause:
                time_since_last_update = self.clock.tick(self.max_fps)
            else:
                time_since_last_update = 0

            # Drawing under the cursor
            if self.leftMouse_down:
                self.toggle_cell(grid)

            # Update the game state
            if time_since_last_update >= 1000 / self.max_fps:
                self.draw(grid)

                # Prepare the next state
                grid.count_neighbors()
                grid.update_grid()

            # Handle events
            for event in pygame.event.get():
                # Quit the game when the user closes the window
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Quit the game when the escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Pause the game when the space bar is pressed
                    elif event.key == pygame.K_SPACE:
                        if self.pause:
                            self.pause = False
                        else:
                            self.pause = True
                    # Regenerate the grid
                    elif event.key == pygame.K_RETURN:
                        grid.generate()
                        self.draw(grid)
                # Toggle cells on when the left mouse button is held down
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftMouse_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftMouse_down = False

        # Clean up Pygame resources
        pygame.quit()


def main():
    # Create a grid
    grid = Grid((150, 300), 5)
    GameApp(grid).game_loop(grid)


if __name__ == "__main__":
    main()
