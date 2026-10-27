
import random
from collections import deque

from settings import WALL_DENSITY


def reachable(start, goal, walls, rows, cols):
    queue = deque([start])
    visited = {start}

    while queue:
        row, col = queue.popleft()

        if (row, col) == goal:
            return True

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            neighbor = (nr, nc)

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if neighbor in walls or neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return False


def generate_maze(rows, cols, start, goal, density=WALL_DENSITY):
    # Try several random layouts until a solvable one is found.
    for _ in range(100):
        walls = set()

        for row in range(rows):
            for col in range(cols):
                cell = (row, col)

                if cell in (start, goal):
                    continue

                if random.random() < density:
                    walls.add(cell)

        if reachable(start, goal, walls, rows, cols):
            return walls

    # Safe fallback: an empty maze is always solvable.
    return set()
