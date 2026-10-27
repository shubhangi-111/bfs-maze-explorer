
import sys
import time
import pygame

from settings import *
from bfs import BFS
from maze import generate_maze


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

pygame.init()
pygame.display.set_caption("BFS Maze Explorer")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 16)
SMALL = pygame.font.SysFont("consolas", 12)
TITLE = pygame.font.SysFont("consolas", 23, bold=True)
BUTTON_FONT = pygame.font.SysFont("consolas", 13, bold=True)

GRID_X = MARGIN
GRID_Y = HEADER_HEIGHT + MARGIN
GRID_W = COLS * CELL_SIZE
GRID_H = ROWS * CELL_SIZE
PANEL_X = GRID_X + GRID_W + MARGIN

start = (1, 1)
goal = (ROWS - 2, COLS - 2)

wall_density = WALL_DENSITY
walls = generate_maze(ROWS, COLS, start, goal, wall_density)

search = None
searching = False
search_delay = 0
search_time = 0.0

status = "Ready - press Run Search"
status_color = MUTED

stick_pos = None
path_index = 0
moving = False
walk_frame = 0
move_target = None
move_one_requested = False

path_animation = []
backtrack_index = 0
backtracking = False

drawing_wall = False
erasing_wall = False
placing_start = False
placing_goal = False

buttons = {}


# --------------------------------------------------
# SEARCH MANAGEMENT
# --------------------------------------------------

def reset_search(message="Search reset"):
    global search, searching, search_time
    global stick_pos, path_index, moving, move_target
    global move_one_requested, path_animation
    global backtrack_index, backtracking, search_delay
    global status, status_color

    search = None
    searching = False
    search_time = 0.0

    stick_pos = None
    path_index = 0
    moving = False
    move_target = None
    move_one_requested = False

    path_animation = []
    backtrack_index = 0
    backtracking = False
    search_delay = 0

    status = message
    status_color = MUTED


def new_maze():
    global walls

    reset_search("Generating new maze...")

    walls = generate_maze(
        ROWS, COLS, start, goal, wall_density
    )


def begin_search():
    global search, searching, search_time
    global status, status_color, stick_pos

    reset_search("Searching...")

    search = BFS(start, goal, walls, ROWS, COLS)
    searching = True
    search_time = time.perf_counter()
    stick_pos = cell_center(start)

    status = "BFS is exploring the maze"
    status_color = CURRENT_COLOR


def finish_search(result):
    global searching, search_time
    global status, status_color
    global path_animation, backtracking, backtrack_index

    searching = False
    search_time = time.perf_counter() - search_time

    if result == "found":
        path_animation = list(reversed(search.path))
        backtrack_index = 0
        backtracking = True

        status = "Goal found - reconstructing path"
        status_color = SUCCESS
    else:
        status = "No path exists!"
        status_color = ERROR


def advance_search():
    global status, status_color

    if search is None or search.finished:
        return

    result = search.step()

    if result in ("found", "no_path"):
        finish_search(result)
    else:
        status = f"Exploring {search.current}"
        status_color = CURRENT_COLOR


# --------------------------------------------------
# GRID HELPERS
# --------------------------------------------------

def grid_cell_at(pos):
    x, y = pos

    if not (GRID_X <= x < GRID_X + GRID_W):
        return None

    if not (GRID_Y <= y < GRID_Y + GRID_H):
        return None

    col = (x - GRID_X) // CELL_SIZE
    row = (y - GRID_Y) // CELL_SIZE

    return int(row), int(col)


def cell_center(cell):
    row, col = cell

    return (
        GRID_X + col * CELL_SIZE + CELL_SIZE // 2,
        GRID_Y + row * CELL_SIZE + CELL_SIZE // 2,
    )


# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

def button_rect(name, y, label, width=None):
    if width is None:
        width = PANEL_WIDTH - 20

    rect = pygame.Rect(PANEL_X + 10, y, width, 30)
    buttons[name] = (rect, label)

    return rect


def draw_button(name, mouse_pos):
    rect, label = buttons[name]

    color = (
        BUTTON_HOVER
        if rect.collidepoint(mouse_pos)
        else BUTTON_COLOR
    )

    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(
        screen, GRID_LINE, rect, 1, border_radius=6
    )

    text = BUTTON_FONT.render(label, True, WHITE)
    screen.blit(text, text.get_rect(center=rect.center))


def draw_small_button(name, mouse_pos):
    rect, label = buttons[name]

    color = (
        BUTTON_HOVER
        if rect.collidepoint(mouse_pos)
        else BUTTON_COLOR
    )

    pygame.draw.rect(screen, color, rect, border_radius=5)

    pygame.draw.rect(
        screen, GRID_LINE, rect, 1, border_radius=5
    )

    text = BUTTON_FONT.render(label, True, WHITE)
    screen.blit(text, text.get_rect(center=rect.center))


# --------------------------------------------------
# CHARACTER DRAWING
# --------------------------------------------------

def draw_stickman(center, moving_now=False):
    x, y = int(center[0]), int(center[1])
    color = WHITE

    phase = walk_frame % 2 if moving_now else 0

    # Head
    pygame.draw.circle(
        screen, color, (x, y - 6), 3
    )

    # Body
    pygame.draw.line(
        screen, color, (x, y - 3), (x, y + 5), 2
    )

    arm_offset = 3 if phase else -3
    leg_offset = 3 if phase else -3

    # Arms
    pygame.draw.line(
        screen,
        color,
        (x, y),
        (x - 4, y + arm_offset),
        2,
    )

    pygame.draw.line(
        screen,
        color,
        (x, y),
        (x + 4, y - arm_offset),
        2,
    )

    # Legs
    pygame.draw.line(
        screen,
        color,
        (x, y + 5),
        (x - 4, y + 10 + leg_offset),
        2,
    )

    pygame.draw.line(
        screen,
        color,
        (x, y + 5),
        (x + 4, y + 10 - leg_offset),
        2,
    )


def draw_flag(center):
    x, y = int(center[0]), int(center[1])

    pygame.draw.line(
        screen, WHITE, (x, y - 9), (x, y + 9), 2
    )

    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (x, y - 9),
            (x + 9, y - 6),
            (x, y - 2),
        ],
    )


# --------------------------------------------------
# GRID RENDERING
# --------------------------------------------------

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            cell = (row, col)
            color = GRID_BG

            if cell in walls:
                color = WALL_COLOR

            if search:
                if cell in search.visited:
                    color = OPEN_COLOR

                if cell in search.explored:
                    color = EXPLORED_COLOR

                if cell == search.current:
                    color = CURRENT_COLOR

                if cell in search.path and not backtracking:
                    color = PATH_COLOR

            rect = pygame.Rect(
                GRID_X + col * CELL_SIZE,
                GRID_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)

    # Animate reconstruction from goal toward start.
    if backtracking and path_animation:
        for cell in path_animation[:backtrack_index + 1]:
            rect = pygame.Rect(
                GRID_X + cell[1] * CELL_SIZE + 3,
                GRID_Y + cell[0] * CELL_SIZE + 3,
                CELL_SIZE - 6,
                CELL_SIZE - 6,
            )

            pygame.draw.rect(
                screen,
                PATH_COLOR,
                rect,
                border_radius=4,
            )

    # Draw start and goal markers.
    start_rect = pygame.Rect(
        GRID_X + start[1] * CELL_SIZE,
        GRID_Y + start[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )

    goal_rect = pygame.Rect(
        GRID_X + goal[1] * CELL_SIZE,
        GRID_Y + goal[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )

    pygame.draw.rect(
        screen, START_COLOR, start_rect, border_radius=4
    )

    pygame.draw.rect(
        screen, GOAL_COLOR, goal_rect, border_radius=4
    )

    # Draw the character only once, at its current position.
    if stick_pos is not None:
        draw_stickman(stick_pos, moving_now=moving)
    else:
        draw_stickman(cell_center(start))

    draw_flag(cell_center(goal))


# --------------------------------------------------
# SIDE PANEL
# --------------------------------------------------

def draw_panel(mouse_pos):
    panel = pygame.Rect(
        PANEL_X, GRID_Y, PANEL_WIDTH, GRID_H
    )

    pygame.draw.rect(
        screen, PANEL_BG, panel, border_radius=10
    )

    x = PANEL_X + 12
    y = GRID_Y + 12

    def text_line(label, color=WHITE, font=FONT, gap=20):
        nonlocal y

        surface = font.render(label, True, color)
        screen.blit(surface, (x, y))
        y += gap

    # Main controls
    text_line("CONTROLS", SUCCESS, TITLE, 32)

    controls = [
        ("run", "Pause Search" if searching else "Run Search"),
        ("step", "Next Step"),
        ("move", "Move One Cell"),
        ("reset", "Reset Search"),
        ("shuffle", "Reshuffle Maze"),
    ]

    for name, label in controls:
        button_rect(name, y, label)
        draw_button(name, mouse_pos)
        y += 35

    # Wall density controls
    y += 4
    text_line("WALL DENSITY", CURRENT_COLOR, FONT, 21)
    text_line(f"{wall_density:.0%}", WHITE, SMALL, 17)

    buttons["density_minus"] = (
        pygame.Rect(x, y, 30, 25), "-"
    )

    buttons["density_plus"] = (
        pygame.Rect(x + 40, y, 30, 25), "+"
    )

    draw_small_button("density_minus", mouse_pos)
    draw_small_button("density_plus", mouse_pos)

    y += 33

    # Statistics
    text_line("STATISTICS", SUCCESS, FONT, 22)

    visited_count = len(search.visited) if search else 0
    explored_count = len(search.explored) if search else 0
    queue_count = len(search.queue) if search else 0
    path_length = (
        len(search.path) - 1
        if search and search.path
        else 0
    )

    text_line(f"Visited: {visited_count}", WHITE, SMALL, 17)
    text_line(f"Expanded: {explored_count}", WHITE, SMALL, 17)
    text_line(f"Queue: {queue_count}", WHITE, SMALL, 17)
    text_line(f"Path: {path_length} moves", WHITE, SMALL, 17)
    text_line(f"Time: {search_time:.4f}s", WHITE, SMALL, 17)

    # Legend
    y += 4
    text_line("LEGEND", CURRENT_COLOR, FONT, 21)

    legend_items = [
        (WALL_COLOR, "Wall"),
        (OPEN_COLOR, "Discovered"),
        (EXPLORED_COLOR, "Expanded"),
        (CURRENT_COLOR, "Current node"),
        (PATH_COLOR, "Shortest path"),
        (START_COLOR, "Start"),
        (GOAL_COLOR, "Goal"),
    ]

    for color, label in legend_items:
        pygame.draw.rect(
            screen,
            color,
            (x, y + 2, 12, 12),
            border_radius=3,
        )

        screen.blit(
            SMALL.render(label, True, MUTED),
            (x + 20, y),
        )

        y += 17


# --------------------------------------------------
# BUTTON ACTIONS
# --------------------------------------------------

def handle_button(name):
    global searching, status, status_color
    global move_one_requested, wall_density

    if name == "run":
        if search is None or search.finished:
            begin_search()
        else:
            searching = not searching

            status = (
                "Searching..."
                if searching
                else "Search paused"
            )

            status_color = CURRENT_COLOR

    elif name == "step":
        if search is None:
            begin_search()
            advance_search()
        elif not search.finished:
            advance_search()

    elif name == "move":
        if (
            search
            and search.found
            and not moving
            and not backtracking
        ):
            move_one_requested = True
        else:
            status = "Find a path first"
            status_color = ERROR

    elif name == "reset":
        reset_search()

    elif name == "shuffle":
        new_maze()

    elif name == "density_minus":
        wall_density = max(
            MIN_WALL_DENSITY,
            wall_density - 0.05,
        )
        new_maze()

    elif name == "density_plus":
        wall_density = min(
            MAX_WALL_DENSITY,
            wall_density + 0.05,
        )
        new_maze()


# --------------------------------------------------
# ANIMATION UPDATES
# --------------------------------------------------

def update():
    global searching, search_delay, status, status_color
    global backtracking, backtrack_index
    global stick_pos, path_index, moving, walk_frame
    global move_target, move_one_requested

    # Automatic BFS exploration
    if searching and search:
        search_delay += 1

        if search_delay >= SEARCH_DELAY:
            search_delay = 0
            advance_search()

    # Animate parent-chain reconstruction
    if backtracking:
        backtrack_index += 1

        if backtrack_index >= len(path_animation):
            backtracking = False
            stick_pos = cell_center(start)
            path_index = 0

            status = "Path found - ready to move"
            status_color = SUCCESS

    # Manual movement along the discovered path
    if search and search.found and not backtracking:
        if move_one_requested and not moving:
            if path_index < len(search.path) - 1:
                path_index += 1

                move_target = cell_center(
                    search.path[path_index]
                )

                moving = True
                move_one_requested = False
            else:
                status = "Destination reached!"
                status_color = SUCCESS
                move_one_requested = False

        if moving and move_target is not None:
            x, y = stick_pos
            tx, ty = move_target

            dx = tx - x
            dy = ty - y
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= MOVE_SPEED:
                stick_pos = (tx, ty)
                moving = False
                move_target = None

                if path_index == len(search.path) - 1:
                    status = "Destination reached!"
                    status_color = SUCCESS
            else:
                stick_pos = (
                    x + dx / distance * MOVE_SPEED,
                    y + dy / distance * MOVE_SPEED,
                )

                walk_frame += 1


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

def main():
    global drawing_wall, erasing_wall
    global placing_start, placing_goal
    global start, goal, walls

    running = True

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cell = grid_cell_at(event.pos)

                    if cell is not None:
                        if cell == start:
                            placing_start = True

                        elif cell == goal:
                            placing_goal = True

                        elif cell not in (start, goal):
                            drawing_wall = True
                            walls.add(cell)

                            reset_search(
                                "Maze edited - run search again"
                            )

                    else:
                        for name, (rect, _) in list(buttons.items()):
                            if rect.collidepoint(event.pos):
                                handle_button(name)
                                break

                elif event.button == 3:
                    cell = grid_cell_at(event.pos)

                    if cell is not None:
                        erasing_wall = True
                        walls.discard(cell)

                        reset_search(
                            "Maze edited - run search again"
                        )

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing_wall = False
                erasing_wall = False
                placing_start = False
                placing_goal = False

            elif event.type == pygame.MOUSEMOTION:
                cell = grid_cell_at(event.pos)

                if cell is not None:
                    if drawing_wall and cell not in (start, goal):
                        walls.add(cell)
                        reset_search(
                            "Maze edited - run search again"
                        )

                    elif erasing_wall:
                        walls.discard(cell)
                        reset_search(
                            "Maze edited - run search again"
                        )

                    elif placing_start and cell != goal:
                        start = cell
                        walls.discard(cell)

                        reset_search(
                            "Start moved - run search again"
                        )

                    elif placing_goal and cell != start:
                        goal = cell
                        walls.discard(cell)

                        reset_search(
                            "Goal moved - run search again"
                        )

        update()

        screen.fill(BACKGROUND)

        title_surface = TITLE.render(
            "BFS MAZE EXPLORER", True, WHITE
        )

        screen.blit(title_surface, (MARGIN, 17))

        subtitle = SMALL.render(
            "Breadth-First Search | FIFO queue | Unit-cost grid",
            True,
            MUTED,
        )

        screen.blit(subtitle, (MARGIN, 44))

        draw_grid()
        draw_panel(mouse_pos)

        status_surface = SMALL.render(
            status, True, status_color
        )

        screen.blit(
            status_surface,
            (MARGIN, GRID_Y + GRID_H + 12),
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
