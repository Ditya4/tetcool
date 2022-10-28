import pygame
from random import choice
from time import time
import numpy as np


'''
We create an array for our game field, filled with integer values, every value
is a color which is equivalent to number.
0 - black
1 - red
2 - blue
3 - yellow
4 - green
Which we'll gonna use for saving already dropped stiks and while dropping if we
have possibility to move dropping stick to the left or right and when stick
should stop falling down.
[[0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0]]
'''


class Brick():

    def __init__(self, canvas, size, color, x, y):
        self.canvas = canvas
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        pygame.draw.rect(self.canvas, self.color,
                         (self.x, self.y, self.size, self.size))


class Stick():

    def __init__(self, canvas, size, colors, x, y):
        '''
        by default in self.bricks we put y(vertical coordinate) of every brick
        and after creating a specific brick we but there certain brick
        '''
        self.canvas = canvas
        self.size = size
        self.colors = colors
        self.x = x
        self.y = y
        self.bricks = [0, self.size, 2*self.size]
        for i in range(len(self.bricks)):
            self.bricks[0] = Brick(self.canvas,
                                   self.size,
                                   self.colors[i],
                                   self.x, self.y + self.bricks[i])


def swich_colors(color_sequence):
    result_sequence = color_sequence[:]
    swiched_color = result_sequence.pop(0)
    result_sequence.append(swiched_color)
    return result_sequence


def to_num(stick_colors):
    '''
    1 - red
    2 - blue
    3 - yellow
    4 - green
    '''
    colors = {"red": 1, "blue": 2, "yellow": 3, "green": 4}
    result = []
    for color in stick_colors:
        result.append(colors[color])
    return result


def get_coords(x, y):
    '''
    [[0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0 0 0 0 0]]
    '''
    print(x // size, y // size)
    return x // size, y // size


def add_stick(table, stick):
    x = stick.x
    y = stick.y
    colors = to_num(stick.colors)
    print(colors)
    print(x, y, colors)
    index_x, index_y = get_coords(x, y)
    print(index_x, index_y)
    for i in range(3):
        table[index_y + i - 1][index_x] = colors[i]
        print(table)
    return table


def draw_table(table):
    # global win
    colors = {1: "red", 2: "blue", 3: "yellow", 4: "green"}
    for i in range(rows):
        for j in range(columns):
            if table[i][j]:
                print(i * size, j * size, table[i][j], colors[table[i][j]])
                pygame.draw.rect(win, colors[table[i][j]],
                                 (j * size, i * size, size, size))
                # Brick(win, size, colors[table[i][j]], x, y)
            # print(table[i][j], end="")
        # print()
    # print()


rows = 15
columns = 11
table = np.zeros(rows * columns, np.int32). reshape(rows, columns)
print(table)


pygame.init()
size = 40
window_height = size * rows
window_width = size * columns
default_x = (window_width - size) // 2
x = default_x
default_y = 0
y = default_y

colors = ["red", "blue", "yellow", "green"]
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Telcool")
start = time()
run = True
stick_count = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0, 0, 0))
    draw_table(table)

    if not stick_count:
        colors_sequence = [choice(colors), choice(colors), choice(colors)]
        stick_count = 1
    stick = Stick(win, size, colors_sequence, x, y)
    if stick.y + size * 3 <= window_height:
        # pass
        # print(time() - start)
        if time() - start > 1:
            y += size
            start = time()
    else:
        stick_count = 0
        table = add_stick(table, stick)
        print(stick.x, stick.y, stick.colors)
        print(table)
        x = default_x
        y = default_y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if stick.x - size >= 0:
            x -= size

    if keys[pygame.K_RIGHT]:
        if stick.x + size < window_width:
            x += size

    if keys[pygame.K_UP]:
        colors_sequence = swich_colors(colors_sequence)
        # win.fill((0, 0, 0))
        # stick = Stick(win, size, colors_sequence, x, y)
        # pygame.display.update()
        # pygame.time.delay(90)

    if keys[pygame.K_SPACE]:
        y = window_height - size * 3
        # stick_count = 0
        # win.fill((0, 0, 0))
        # stick = Stick(win, size, colors_sequence, x, y)
        # pygame.display.update()
        # pygame.time.delay(30)

    pygame.display.update()
    pygame.time.delay(50)

pygame.quit()
