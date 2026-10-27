# BFS Maze Explorer 🧩

An interactive maze-solving application built with **Python and Pygame**, demonstrating the Breadth-First Search (BFS) algorithm through animated exploration, shortest-path reconstruction, and a moving stickman character.

Watch the algorithm explore a maze level by level, discover a route to the destination, and guide the stickman along the shortest path.

## ✨ Features

- **BFS Pathfinding:** Finds a shortest path in an unweighted grid using Breadth-First Search.
- **Interactive Visualization:** Watch discovered and explored cells update in real time.
- **Step-by-Step Execution:** Advance the algorithm one node expansion at a time.
- **Animated Path Reconstruction:** Visualizes the process of tracing parent pointers backward from the goal.
- **Stickman Animation:** Move the stickman along the final path, one grid cell at a time.
- **Random Maze Generation:** Generate new maze layouts with adjustable obstacle density.
- **Interactive Grid Editing:** Draw walls, erase obstacles, and reposition the start and destination.
- **Search Statistics:** View visited nodes, expanded nodes, queue size, path length, and elapsed search time.
- **Unreachable Goal Detection:** Detects when no valid path exists.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application logic and algorithm implementation |
| Pygame | Graphics, user interaction, and animation |
| `collections.deque` | FIFO queue for BFS traversal |
| `time` | Measuring search execution time |

## 📁 Project Structure

```text
bfs-maze-explorer/
├── main.py        # Graphical interface and animation
├── bfs.py         # Breadth-First Search implementation
├── maze.py        # Maze generation and reachability checks
├── settings.py    # Grid dimensions, colors, and configuration
└── README.md      # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later recommended
- pip
- A desktop environment capable of running Pygame

### Installation

**1. Clone the repository** (if you've uploaded it to GitHub):

```bash
git clone <your-repository-url>
cd bfs-maze-explorer
```

Alternatively, open your existing project directory.

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment**

Windows — Git Bash:

```bash
source .venv/Scripts/activate
```

Windows — Command Prompt:

```bat
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

**4. Install the dependency**

```bash
python -m pip install pygame
```

**5. Launch the application**

```bash
python main.py
```

## 🎮 Controls

| Action | Control |
|---|---|
| Start automatic search | Run Search |
| Pause or resume search | Run Search |
| Advance one BFS expansion | Next Step |
| Move the stickman one grid cell | Move One Cell |
| Clear the current search | Reset Search |
| Generate another maze | Reshuffle Maze |
| Increase or decrease obstacle density | `+` / `−` |
| Add walls | Left-click or drag on the grid |
| Remove walls | Right-click or drag on the grid |
| Reposition start or goal | Drag their grid cells |

## 🧠 How the Algorithm Works

Breadth-First Search is an uninformed graph traversal algorithm that explores nodes in increasing order of their distance from the starting node.

The application represents each traversable grid cell as a node and each valid movement between adjacent cells as an edge.

### Algorithm workflow

1. Initialize a FIFO queue with the starting node.
2. Mark the start as visited and initialize its parent pointer.
3. Remove the oldest node from the queue.
4. If the removed node is the destination, reconstruct the path.
5. Otherwise, discover its unvisited, traversable neighbours, record their parents, and enqueue them.
6. Repeat until the destination is found or the queue becomes empty.

### Shortest-path reconstruction

Each discovered node stores a reference to the node from which it was reached. Once the destination is found, these parent references are followed backward to the start. Reversing the resulting sequence gives the route from start to destination.

### Complexity Analysis

Let \(V\) denote the number of vertices and \(E\) the number of edges in the graph.

- **Time complexity:** \(O(V + E)\)
- **Space complexity:** \(O(V)\)

For a grid with four-directional movement, each cell has at most four neighbours. BFS therefore finds a shortest path when every movement has the same cost.

## 📊 Visualization Legend

| Visual element | Meaning |
|---|---|
| Stickman | Starting character and path execution |
| Flag | Destination |
| Grey cells | Obstacles |
| Blue cells | Discovered nodes |
| Dark blue cells | Expanded nodes |
| Orange cell | Current node being explored |
| Yellow cells | Reconstructed shortest path |
| Green cell | Start position |
| Red cell | Goal position |

## 🧪 Suggested Test Cases

1. **Open grid:** Verify that BFS reaches the destination and returns a shortest path.
2. **Obstacle navigation:** Add walls and confirm that the algorithm finds an alternate route.
3. **Unreachable destination:** Block every possible route and verify that the application reports failure.
4. **Step-by-step execution:** Confirm that each Next Step action expands at most one node.
5. **Random maze generation:** Generate multiple layouts and verify that the start and destination remain valid.
6. **Interactive editing:** Move the endpoints and change obstacles before starting a new search.

## 🎯 Learning Outcomes

This project demonstrates:

- Graph traversal and uninformed search.
- FIFO queue operations and visited-state management.
- Parent-pointer tracking and path reconstruction.
- Shortest-path guarantees for unweighted graphs.
- Interactive algorithm visualization and event-driven programming.
- Experimental observation of search behaviour across different maze configurations.

## 🔮 Future Improvements

- Compare BFS with Depth-First Search and Dijkstra's algorithm.
- Add maze-generation algorithms.
- Display the queue contents and current node's neighbours.
- Record search metrics across multiple maze configurations.
- Add configurable grid dimensions and movement rules.

## 👩‍💻 Author

Developed as an Artificial Intelligence and Search Concepts (AISC) academic assignment.

---

**Note:** BFS guarantees a shortest path in terms of the number of edges for unweighted graphs. It does not necessarily minimize total cost when different movements have different costs.