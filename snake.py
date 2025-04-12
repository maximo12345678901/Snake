import time 
import random
import keyboard # type: ignore
import os

xMapSize = int(input("x: "))
yMapSize = int(input("y: "))

time.sleep(1)

segments = [
    [xMapSize // 2, yMapSize // 2],
    [xMapSize // 2, yMapSize // 2 + 1],
    [xMapSize // 2, yMapSize // 2 + 2],
    [xMapSize // 2, yMapSize // 2 + 3]
]
direction = [0, -1]

ITERATION_DURATION = 0.15
grow_buffer = 0
timer = 0

def spawn_food():
    while True:
        pos = [random.randint(0, xMapSize - 1), random.randint(0, yMapSize - 1)]
        if pos not in segments:
            return pos

apple = spawn_food()
gold_apple = [-1, -1]

gold_apple_direction = [0, 0]

score = 0
game_over = False

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

def Rendering():
    print("Snake")
    print(" "+"__" * xMapSize)
    for y in range(yMapSize):
        row = ["|"]
        for x in range(xMapSize):
            if [x, y] == segments[0]:
                row.append("\033[32m()\033[0m")
            elif [x, y] in segments:
                row.append("\033[32m[]\033[0m")
            elif [x, y] == apple:
                row.append("\033[31m()\033[0m")
            elif [x, y] == gold_apple:
                row.append("\033[33m()\033[0m")
            else:
                row.append("  \033[0m")
        row.append("|")
        print("".join(row))
    print(" "+"--" * xMapSize)
    print("Score: " + str(score))

while True:
    os.system("cls" or "clear")
    Input()
    new_head = [segments[0][0] + direction[0], segments[0][1] + direction[1]]

    if new_head in segments or new_head[0] < 0 or new_head[0] >= xMapSize or new_head[1] < 0 or new_head[1] >= yMapSize:
        game_over = True

    segments.insert(0, new_head)

    if new_head == apple:
        ITERATION_DURATION *= 0.99
        score += 1
        grow_buffer += 1

        if random.randint(1, 5) == 1:
            gold_apple = spawn_food()
            apple = [-1, -1]
        else:
            apple = spawn_food()
            gold_apple = [-1, -1]

    elif new_head == gold_apple:
        ITERATION_DURATION *= 0.95
        score += 5
        grow_buffer += 5
        apple = spawn_food()
        gold_apple = [-1, -1]

    if not grow_buffer > 0:
        segments.pop()
    else:
        grow_buffer -= 1

        
    gold_apple_direction = [random.randint(-1, 1),  random.randint(-1, 1)]

    if gold_apple != [-1, -1]:
        new_gold_apple_pos = [gold_apple[0] + gold_apple_direction[0], gold_apple[1] + gold_apple_direction[1]]
        if new_gold_apple_pos not in segments and new_gold_apple_pos[0] >= 0 and new_gold_apple_pos[0] < xMapSize and new_gold_apple_pos[1] >= 0 and new_gold_apple_pos[1] < yMapSize:
            gold_apple = new_gold_apple_pos

    Rendering()
    time.sleep(ITERATION_DURATION)
    if game_over == True:
        time.sleep(2)
        break

