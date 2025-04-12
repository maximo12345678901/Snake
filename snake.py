import time 
import random
import keyboard # type: ignore
import os

# Ask the user for the map size
xMapSize = int(input("x: "))
yMapSize = int(input("y: "))

# Give the user a bit of time before the game begins
time.sleep(1)

# Initialize color codes
reset_color = "\033[0m"
red = "\033[31m"
green = "\033[32m"
gold = "\033[33m"

# Initialize the first four segments of the snake before the game loop begins
segments = [
    [xMapSize // 2, yMapSize // 2],
    [xMapSize // 2, yMapSize // 2 + 1],
    [xMapSize // 2, yMapSize // 2 + 2],
    [xMapSize // 2, yMapSize // 2 + 3]
]

direction = [0, -1] # The player starts facing up

ITERATION_DURATION = 0.15 # The time in between movement steps
grow_buffer = 0
timer = 0

# A function that keeps generating a random position within the playing field, and returns it when it's unoccupied
def spawn_food():
    while True:
        pos = [random.randint(0, xMapSize - 1), random.randint(0, yMapSize - 1)]
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
    print(" "+"__" * xMapSize) # Draw the upper border of the playing field
    for y in range(yMapSize):
        row = ["|"] # Draw the left border of the playing field
        for x in range(xMapSize):
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
    print(" "+"--" * xMapSize) # Draw the bottom border of the playing field
    print("Score: " + str(score))

while True:
    os.system("cls" or "clear") # Clear the terminal screen before drawing 
    Input()
    new_head = [segments[0][0] + direction[0], segments[0][1] + direction[1]] # The position of the new head will be the old head + the direction

    if new_head in segments or new_head[0] < 0 or new_head[0] >= xMapSize or new_head[1] < 0 or new_head[1] >= yMapSize:
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
        if new_gold_apple_pos not in segments and new_gold_apple_pos[0] >= 0 and new_gold_apple_pos[0] < xMapSize and new_gold_apple_pos[1] >= 0 and new_gold_apple_pos[1] < yMapSize:
            gold_apple = new_gold_apple_pos

    Rendering()
    time.sleep(ITERATION_DURATION)
    if game_over == True:
        time.sleep(2) # Give the played time to realise that they are a failure
        break

