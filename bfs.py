
from collections import deque


class BFS:
    def __init__(self, start, goal, walls, rows, cols):
        self.start = start
        self.goal = goal
        self.walls = walls
        self.rows = rows
        self.cols = cols

        self.queue = deque([start])
        self.visited = {start}
        self.parent = {start: None}

        self.current = None
        self.explored = []
        self.path = []

        self.finished = False
        self.found = False
        self.steps = 0

    def get_neighbors(self, node):
        row, col = node

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        neighbors = []

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            neighbor = (nr, nc)

            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                continue

            if neighbor in self.walls or neighbor in self.visited:
                continue

            neighbors.append(neighbor)

        return neighbors

    def reconstruct_path(self):
        node = self.goal
        path = []

        while node is not None:
            path.append(node)
            node = self.parent[node]

        self.path = path[::-1]

    def step(self):
        if self.finished:
            return "finished"

        if not self.queue:
            self.finished = True
            self.found = False
            return "no_path"

        self.current = self.queue.popleft()
        self.explored.append(self.current)
        self.steps += 1

        if self.current == self.goal:
            self.reconstruct_path()
            self.finished = True
            self.found = True
            return "found"

        for neighbor in self.get_neighbors(self.current):
            self.visited.add(neighbor)
            self.parent[neighbor] = self.current
            self.queue.append(neighbor)

        return "exploring"
