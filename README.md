# BFS Maze Explorer

**BFS Maze Explorer** is an interactive maze-solving application developed using Python and Pygame to demonstrate the Breadth-First Search (BFS) algorithm. It visualizes graph traversal, node exploration, shortest-path reconstruction, and movement through an obstacle-filled grid.

The application allows users to observe the algorithm's behaviour in automatic or step-by-step mode while interacting with the maze and generating new layouts.

## Features

- **Breadth-First Search:** Finds a shortest path in an unweighted grid using a FIFO queue.
- **Step-by-Step Exploration:** Advances the search one node expansion at a time.
- **Automatic Search:** Runs BFS continuously with animated exploration.
- **Path Reconstruction:** Visualizes the process of tracing parent pointers backward from the destination to the starting position.
- **Stickman Animation:** Moves the character along the discovered shortest path, one grid cell at a time.
- **Interactive Maze Editing:** Add and remove obstacles using the mouse.
- **Movable Endpoints:** Reposition the start and destination before running a search.
- **Random Maze Generation:** Generate new obstacle arrangements while preserving the endpoints.
- **Adjustable Wall Density:** Increase or decrease the proportion of randomly generated obstacles.
- **Search Statistics:** Display discovered nodes, expanded nodes, queue size, path length, and elapsed search time.
- **Unreachable Goal Detection:** Reports when the destination cannot be reached.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and BFS implementation |
| Pygame | Graphical interface, input handling, and animation |
| `collections.deque` | FIFO queue used by BFS |
| `random` | Random obstacle generation |
| `time` | Measuring elapsed search time |

## Project Structure

```text
bfs-maze-explorer/
├── main.py       # Graphical interface and animation
├── bfs.py        # Breadth-First Search algorithm
├── maze.py       # Maze generation and reachability checking
├── settings.py   # Configuration and visual settings
└── README.md     # Project documentation
```

## Installation and Execution

### Prerequisites

- Python 3.9 or later
- Pygame or Pygame Community Edition

### Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the graphics dependency:

```bash
python -m pip install pygame
```

If using Pygame Community Edition instead:

```bash
python -m pip install pygame-ce
```

Launch the application:

```bash
python main.py
```

## Controls

| Control | Function |
|---|---|
| Run Search | Start the search or resume a paused search |
| Next Step | Expand one node in the BFS search |
| Move One Cell | Advance the stickman by one grid cell along the discovered path |
| Reset Search | Clear the current search state |
| Reshuffle Maze | Generate a new random obstacle layout |
| `+` / `−` | Adjust wall density and generate a new maze |
| Left-click or drag | Add obstacles to the grid |
| Right-click or drag | Remove obstacles |
| Drag the start or goal | Change the corresponding endpoint |

Editing the maze or moving an endpoint resets the current search state.

## Algorithm Overview

Breadth-First Search is an uninformed graph traversal algorithm that explores nodes in increasing order of their distance from the starting node.

In this application, each traversable grid cell represents a vertex, and movement between adjacent cells represents an edge. Movement is restricted to four directions: up, down, left, and right. Every move has an equal cost.

### Algorithm Steps

1. Initialize a FIFO queue with the starting node.
2. Mark the starting node as visited and assign it no parent.
3. Remove the oldest node from the queue.
4. Check whether the current node is the destination.
5. If the destination has not been reached, discover its valid, unvisited neighbours.
6. Mark newly discovered neighbours as visited, record their parent nodes, and add them to the queue.
7. Repeat until the destination is found or the queue becomes empty.

### Shortest-Path Reconstruction

Each discovered node stores a reference to its parent, which represents the node from which it was first reached.

When the destination is found, the application follows these parent references backward from the goal to the start. The resulting sequence is reversed to obtain the route from start to goal.

The application visualizes this reconstruction separately from the search itself. Once the path has been reconstructed, the stickman can execute the route through individual movement steps.

## Visualization Legend

| Element | Meaning |
|---|---|
| Green cell | Starting position |
| Red cell | Destination |
| Grey cells | Obstacles |
| Blue cells | Discovered nodes |
| Dark blue cells | Expanded nodes |
| Orange cell | Current node |
| Yellow cells | Reconstructed shortest path |
| Stickman | Character executing the route |
| Flag | Destination marker |

## Complexity Analysis

Let \(V\) denote the number of vertices and \(E\) the number of edges in the graph.

- **Time complexity:** \(O(V+E)\)
- **Space complexity:** \(O(V)\)

For a grid with four-directional movement, each vertex has at most four neighbours. BFS finds a shortest path in terms of the number of edges when all movements have equal cost.

## Testing Scenarios

The following scenarios can be used to evaluate the application:

1. **Open grid:** Verify that BFS discovers a shortest route to the destination.
2. **Obstacle navigation:** Add walls and observe how the search explores alternative routes.
3. **Unreachable destination:** Create a barrier that prevents access to the goal and verify that the algorithm reports failure.
4. **Step-by-step execution:** Confirm that each Next Step action expands at most one node.
5. **Random maze generation:** Generate different layouts and observe changes in the exploration process.
6. **Interactive editing:** Change obstacles or endpoints and run a fresh search.
7. **Path execution:** Verify that the stickman follows the reconstructed route without crossing obstacles.

## Learning Outcomes

This project demonstrates:

- Graph traversal and uninformed search.
- FIFO queue operations and visited-node management.
- Parent-pointer tracking and shortest-path reconstruction.
- The relationship between graph structure and search behaviour.
- Interactive visualization of algorithm execution.
- The distinction between finding a solution and executing it.

## Future Improvements

- Compare BFS with Depth-First Search and Dijkstra's algorithm.
- Display the queue contents and the current node's neighbours.
- Add configurable grid dimensions and movement rules.
- Record search statistics across multiple maze configurations.
- Introduce additional maze-generation techniques.

## Author

Developed as an academic assignment for Artificial Intelligence and Search Concepts (AISC).

---

**Note:** BFS guarantees a shortest path by number of moves for an unweighted graph. It does not necessarily find the minimum-cost path when different movements have different costs.
