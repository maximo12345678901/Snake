import curses
import time
import random

# Game settings
x_map_size = 20
y_map_size = 20

ITERATION_DURATION = 0.15

def spawn_food(segments):
    while True:
        pos = [random.randint(0, x_map_size - 1), random.randint(0, y_map_size - 1)]
        if pos not in segments:
            return pos

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)
    stdscr.timeout(int(ITERATION_DURATION * 1000))

    # Color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Apple
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Golden Apple

    # Initial snake
    segments = [
        [x_map_size // 2, y_map_size // 2],
        [x_map_size // 2, y_map_size // 2 + 1],
        [x_map_size // 2, y_map_size // 2 + 2],
        [x_map_size // 2, y_map_size // 2 + 3]
    ]
    direction = [0, -1]
    grow_buffer = 0
    score = 0
    game_over = False
    apple = spawn_food(segments)
    gold_apple = [-1, -1]
    gold_apple_direction = [0, 0]
    iteration_duration = ITERATION_DURATION

    key_map = {
        curses.KEY_UP:    [0, -1],
        curses.KEY_DOWN:  [0, 1],
        curses.KEY_LEFT:  [-1, 0],
        curses.KEY_RIGHT: [1, 0],
        ord('w'):         [0, -1],
        ord('s'):         [0, 1],
        ord('a'):         [-1, 0],
        ord('d'):         [1, 0],
    }

    while not game_over:
        stdscr.clear()
        # Draw borders
        stdscr.addstr(0, 0, " " + "" * x_map_size)
        for y in range(y_map_size):
            stdscr.addstr(y + 1, 0, "|")
            for x in range(x_map_size):
                pos = [x, y]
                if pos == segments[0]:
                    stdscr.addstr(y + 1, x * 2 + 1, "{}", curses.color_pair(1))
                elif pos in segments:
                    stdscr.addstr(y + 1, x * 2 + 1, "[]", curses.color_pair(1))
                elif pos == apple:
                    stdscr.addstr(y + 1, x * 2 + 1, "()", curses.color_pair(2))
                elif pos == gold_apple:
                    stdscr.addstr(y + 1, x * 2 + 1, "()", curses.color_pair(3))
                else:
                    stdscr.addstr(y + 1, x * 2 + 1, "  ")
            stdscr.addstr(y + 1, x_map_size * 2 + 1, "|")
        stdscr.addstr(y_map_size + 1, 1, "--" * x_map_size)
        stdscr.addstr(y_map_size + 2, 0, f"Score: {score}")

        stdscr.refresh()

        # Input
        try:
            key = stdscr.getch()
        except:
            key = -1
        if key in key_map:
            new_dir = key_map[key]
            # Prevent reversing
            if [new_dir[0], new_dir[1]] != [-direction[0], -direction[1]]:
                direction = new_dir

        # Move snake
        new_head = [segments[0][0] + direction[0], segments[0][1] + direction[1]]

        # Check collisions
        if (new_head in segments or
            new_head[0] < 0 or new_head[0] >= x_map_size or
            new_head[1] < 0 or new_head[1] >= y_map_size):
            game_over = True
            continue

        segments.insert(0, new_head)

        if new_head == apple:
            iteration_duration *= 0.99
            score += 1
            grow_buffer += 1
            if random.randint(1, 5) == 1:
                gold_apple = spawn_food(segments)
                apple = [-1, -1]
            else:
                apple = spawn_food(segments)
                gold_apple = [-1, -1]
        elif new_head == gold_apple:
            iteration_duration *= 0.99
            score += 5
            grow_buffer += 5
            apple = spawn_food(segments)
            gold_apple = [-1, -1]

        if grow_buffer > 0:
            grow_buffer -= 1
        else:
            segments.pop()

        # Move golden apple
        gold_apple_direction = [random.randint(-1, 1), random.randint(-1, 1)]
        if gold_apple != [-1, -1]:
            new_gold_apple_pos = [gold_apple[0] + gold_apple_direction[0], gold_apple[1] + gold_apple_direction[1]]
            if (new_gold_apple_pos not in segments and
                0 <= new_gold_apple_pos[0] < x_map_size and
                0 <= new_gold_apple_pos[1] < y_map_size):
                gold_apple = new_gold_apple_pos

        stdscr.timeout(int(iteration_duration * 1000))

    # Game over screen
    stdscr.nodelay(False)
    stdscr.addstr(y_map_size // 2, x_map_size, "GAME OVER! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)