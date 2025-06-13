import time 
import random
import keyboard # type: ignore
import os

# Ask the user for the map size
x_map_size = 20 #int(input("x: "))
y_map_size = 20 #int(input("y: "))

# Give the user a bit of time before the game begins
time.sleep(.1)

# Initialize color codes
reset_color = "\033[0m"
red = "\033[31m"
green = "\033[32m"
gold = "\033[33m"

# Initialize the first four segments of the snake before the game loop begins
segments = [
    [x_map_size // 2, y_map_size // 2],
    [x_map_size // 2, y_map_size // 2 + 1],
    [x_map_size // 2, y_map_size // 2 + 2],
    [x_map_size // 2, y_map_size // 2 + 3]
]

direction = [0, -1] # The player starts facing up

ITERATION_DURATION = 0.15 # The time in between movement steps
time_to_pass = 0

grow_buffer = 0


# A function that keeps generating a random position within the playing field, and returns it when it's unoccupied
def spawn_food():
    while True:
        pos = [random.randint(0, x_map_size - 1), random.randint(0, y_map_size - 1)]
        if pos not in segments:
            return pos

apple = spawn_food() # Set the position of the apple before the game begins
gold_apple = [-1, -1] # Hide the gold apple outside of the playing field

gold_apple_direction = [0, 0] # Define the direction of the golden apple

score = 0
game_over = False

# A procedure that changes the direction of the player according to the player input
def Input():
    global direction
    if (keyboard.is_pressed("w") or keyboard.is_pressed("up")) and direction != [0, 1]:
        direction = [0, -1]
    elif (keyboard.is_pressed("s") or keyboard.is_pressed("down")) and direction != [0, -1]:
        direction = [0, 1]
    elif (keyboard.is_pressed("a") or keyboard.is_pressed("left")) and direction != [1, 0]:
        direction = [-1, 0]
    elif (keyboard.is_pressed("d") or keyboard.is_pressed("right")) and direction != [-1, 0]:
        direction = [1, 0]

# This procedure loops through each y, and within each y it loops through each x,
# if the current [x, y] overlaps any game object it adds a set of characters resembling apples or snake parts to a list
# The list will later be turned into a string which will be printed on the screen
def Rendering():
    print("Snake")
    print(" "+"__" * x_map_size) # Draw the upper border of the playing field
    for y in range(y_map_size):
        row = ["|"] # Draw the left border of the playing field
        for x in range(x_map_size):
            if [x, y] == segments[0]:
                row.append(green + "()" + reset_color) # The head of the snake is "()"
            elif [x, y] in segments:
                row.append(green + "[]" + reset_color) # The rest of the snake is "[]"
            elif [x, y] == apple:
                row.append(red + "()" + reset_color) # Apples are also "()"
            elif [x, y] == gold_apple:
                row.append(gold + "()" + reset_color)
            else:
                row.append("  ") # If there is no game object current [x, y] of the loop, just print spaces
        row.append("|") # Draw the right border of the playing field
        print("".join(row)) # Turn the list into a printable string
    print(" "+"--" * x_map_size) # Draw the bottom border of the playing field
    print("Score: " + str(score))

while True:

    Input()
    if (time.time() > time_to_pass):
        time_to_pass = time.time() + ITERATION_DURATION
        os.system("cls" or "clear") # Clear the terminal screen before drawing 
        new_head = [segments[0][0] + direction[0], segments[0][1] + direction[1]] # The position of the new head will be the old head + the direction

        if new_head in segments or new_head[0] < 0 or new_head[0] >= x_map_size or new_head[1] < 0 or new_head[1] >= y_map_size:
            game_over = True # If the position of the new head overlaps the borders or the snake itself, game over

        segments.insert(0, new_head) # Add the seperate new head position to the list of all snake segments (specifically at the beginning of the list)

        if new_head == apple:
            ITERATION_DURATION *= 0.99 # Increase the speed of which the game plays out
            score += 1
            grow_buffer += 1 # The player will grow with one

            # One in five chance for a golden apple to spawn
            if random.randint(1, 5) == 1: 
                gold_apple = spawn_food()
                apple = [-1, -1] # If a golden apple is spawned, hide the normal apple outside the map
            else:
                apple = spawn_food()
                gold_apple = [-1, -1] # If a normal apple is spawned, hide the golden apple

        elif new_head == gold_apple:
            ITERATION_DURATION *= 0.99
            score += 5
            grow_buffer += 5 
            apple = spawn_food()
            gold_apple = [-1, -1] # Hide the golden apple outside the map regardless, so there cannot be two golden apples in a row

        if not grow_buffer > 0:
            segments.pop() # Remove from the segments list (automatically the last item) if the snake is not supposed to grow
        else:
            grow_buffer -= 1

            
        gold_apple_direction = [random.randint(-1, 1),  random.randint(-1, 1)] # The golden apple has legs

        # If the golden apple isn't hidden, it moves in a random direction
        if gold_apple != [-1, -1]:
            new_gold_apple_pos = [gold_apple[0] + gold_apple_direction[0], gold_apple[1] + gold_apple_direction[1]]
            if new_gold_apple_pos not in segments and new_gold_apple_pos[0] >= 0 and new_gold_apple_pos[0] < x_map_size and new_gold_apple_pos[1] >= 0 and new_gold_apple_pos[1] < y_map_size:
                gold_apple = new_gold_apple_pos

        Rendering()
        if game_over == True:
            break

