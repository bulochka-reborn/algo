import pygame
import random
import heapq
import time

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 600
GRID_SIZE = 10  # Размер поля NxN
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
FIXED_OBSTACLES = [
    (0, 7), (0, 8),
    (1, 0), (1, 3), 
    (2, 4), (2, 7),
    (3, 5), (3, 7),
    (4, 0), (4, 5), 
    (5, 0), (4, 9),
    (6, 4), (6, 6),
    (7, 4), (7, 6), 
    (8, 1), (8, 3),
    (9, 2), (9, 4), 
    (1, 6), (9, 6),
    (7, 7)
]

FIXED_START = (7, 0)
FIXED_END = (9, 9)
pygame.display.set_caption("A*")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Типы ячеек
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
VISITED = 5


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = EMPTY
        self.color = WHITE
        self.neighbors = []

    def reset(self):
        self.state = EMPTY
        self.color = WHITE
        self.neighbors = []

    def make_start(self):
        self.state = START
        self.color = ORANGE

    def make_end(self):
        self.state = END
        self.color = TURQUOISE

    def make_barrier(self):
        self.state = OBSTACLE
        self.color = BLACK

    def make_open(self):
        if self.state not in (START, END):
            self.color = GREEN

    def make_closed(self):
        if self.state not in (START, END):
            self.color = RED

    def make_path(self):
        if self.state not in (START, END):
            self.color = PURPLE

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dir_row, dir_col in directions:
            r = self.row + dir_row
            c = self.col + dir_col

            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                neighbor = grid[r][c]

                if neighbor.state != OBSTACLE:
                    self.neighbors.append(neighbor)

    def draw(self, win):
        rect = pygame.Rect(self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(win, self.color, rect)


def h(x, y):
    return abs(x.row - y.row) + abs(x.col - y.col)


def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid


def draw_grid(win, grid):
    for row in grid:
        for cell in row:
            cell.draw(win)

    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()


def generate_default_grid(grid):
    for row in grid:
        for cell in row:
            cell.reset()

    for row, col in FIXED_OBSTACLES:
        grid[row][col].make_barrier()

    start = grid[FIXED_START[0]][FIXED_START[1]]
    end = grid[FIXED_END[0]][FIXED_END[1]]

    start.make_start()
    end.make_end()

    return start, end


def generate_random_grid(grid):
    # Очищаем сетку
    for row in grid:
        for cell in row:
            cell.reset()

    # Выбираем случайные начальную и конечную точки
    start_row, start_col = random.randint(0, GRID_SIZE - 1), random.randint(
        0, GRID_SIZE - 1
    )
    end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(
        0, GRID_SIZE - 1
    )

    # Убедимся, что начальная и конечная точки разные
    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(
            0, GRID_SIZE - 1
        )

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_start()
    end.make_end()

    # Добавляем случайные препятствия (20% ячеек)
    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.2)
    for _ in range(obstacle_count):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(
            0, GRID_SIZE - 1
        )
        cell = grid[row][col]
        if cell.state != START and cell.state != END:
            cell.make_barrier()

    return start, end


def draw():
    draw_grid(WIN, grid)


def reconstruct_path(came_from, current):
    for cell in came_from.values():
        if cell.state == PATH:
            cell.state = VISITED
            cell.color = RED
        elif cell.color == PURPLE:
            cell.color = RED

    draw()

    time.sleep(0.5)

    while current in came_from:
        current = came_from[current]
        current.make_path()

        draw() # красиво

        time.sleep(0.1)


def a_star_algorithm(draw, grid, start, end):
    opened = []
    came_from = {}

    g = {cell: float('inf') for row in grid for cell in row}
    g[start] = 0

    heapq.heappush(opened, (h(start, end), 0, start.row, start.col, start)) # костыли размером с небоскреб

    while opened:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        _, g_at_push, _, _, curr = heapq.heappop(opened)

        if g_at_push > g[curr]:
            continue

        if curr == end:
            reconstruct_path(came_from, end)
            end.make_end()
            start.make_start()
            return True

        for neighbor in curr.neighbors:
            temp_g = g[curr] + 1

            if temp_g < g[neighbor]:
                came_from[neighbor] = curr

                g[neighbor] = temp_g
                neighbor_f = temp_g + h(neighbor, end)

                heapq.heappush(opened, (neighbor_f, temp_g, neighbor.row, neighbor.col, neighbor))

                neighbor.make_open()

        draw()

        if curr != start:
            curr.make_closed()

    return False

        
grid = make_grid()
start, end = generate_default_grid(grid)

run = True
started = False

while run:
    draw_grid(WIN, grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not started:
                for row in grid:
                    for cell in row:
                        cell.update_neighbors(grid)

                started = a_star_algorithm(draw, grid, start, end)
            if event.key == pygame.K_r:
                grid = make_grid()
                start, end = generate_random_grid(grid)
                started = False

pygame.quit()