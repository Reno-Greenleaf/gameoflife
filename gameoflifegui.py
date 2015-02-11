"""

    CONWAY'S GAME OF LIFE

    this python version was written by
    JP ARMSTRONG http://www.jparmstrong.com/

    I developed this game just to learn python.

    MIT-LICENSE

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#################################################
"""


import pygame, random, time
from pygame.locals import *
from boxes import Box

MAX_X = 80
MAX_Y = 40
SIZE = 10
DEBUG = False
keep_background = False
running = True
button_down = False
boxes = []
board = []
screen = False
keys = False
button_down = False
button_type = False
sx = False
sy = False
mouse_x = False
mouse_y = False
rand_col = False

def borderless(n, t):
    """ Allowing the board to wrap around, "infinite playing field". """

    if n < 0:
        n = t + n;
    elif n >= t:
        n = abs(n) % t

    return n

def rulesOfLife(b):
    """ The rules to Life. """

    total_pop = 0;

    pop_list = ['0'] * MAX_X
    
    for i in range(MAX_X):
        pop_list[i] = ['0'] * MAX_Y

   # Checking to see what is populated around each cell.
    for y in range(MAX_Y):
        for x in range(MAX_X):

            pop = 0
            buf = []

            # row A
            if b[borderless(x-1, MAX_X)][borderless(y-1, MAX_Y)] == True:
                buf.append("a1 ")
                pop += 1
                
            if b[borderless(x, MAX_X)][borderless(y-1, MAX_Y)] == True:
                buf.append("a2 ")
                pop += 1
                
            if b[borderless(x+1, MAX_X)][borderless(y-1, MAX_Y)] == True:
                buf.append("a3 ")
                pop += 1

            # row B
            if b[borderless(x-1, MAX_X)][borderless(y, MAX_Y)] == True:
                buf.append("b1 ")
                pop += 1
            if b[borderless(x+1, MAX_X)][borderless(y, MAX_Y)] == True:
                buf.append("b3 ")
                pop += 1

            # row C
            if b[borderless(x-1, MAX_X)][borderless(y+1, MAX_Y)] == True:
                buf.append("c1 ")
                pop += 1
                
            if b[borderless(x, MAX_X)][borderless(y+1, MAX_Y)] == True:
                buf.append("c2 ")
                pop += 1
                
            if b[borderless(x+1, MAX_X)][borderless(y+1, MAX_Y)] == True:
                buf.append("c3 ")
                pop += 1

            if DEBUG and pop > 0:
                print x,y,":",''.join(buf),pop

            total_pop += pop

            pop_list[x][y] = pop

    
    # Now that we know whats around each cell, we implement the rules of Life.
    for y in range(MAX_Y):
        for x in range(MAX_X):

            if b[x][y] == True and (pop_list[x][y] < 2 or pop_list[x][y] > 3):
                b[x][y] = False
                
            elif b[x][y] == False and pop_list[x][y] == 3:
                b[x][y] = True


def updateDisplay():
    for dy in range(MAX_Y):
        for dx in range(MAX_X):
            if board[dx][dy] == True:
                if rand_col:
                    boxes[dx][dy] = Box([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], [dx * SIZE, dy * SIZE], SIZE)
                else:
                    boxes[dx][dy] = Box([255, 255, 255], [dx * SIZE, dy * SIZE], SIZE)
            elif not keep_background:
                boxes[dx][dy] = Box([0, 0, 0], [dx * SIZE, dy * SIZE], SIZE)

            screen.blit(boxes[dx][dy].image, boxes[dx][dy].rect)
    
    pygame.display.update()

# Making the boxes.
boxes = [''] * MAX_X
    
for i in range(MAX_X):
    boxes[i] = [''] * MAX_Y

pygame.init()
pygame.display.set_caption('Conway\'s Game of Life by jparmstrong.com')
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])


# Making the board.
board = [False] * MAX_X
    
for i in range(MAX_X):
    board[i] = [False] * MAX_Y

keys = pygame.key.get_pressed()


while running:
    for event in pygame.event.get():

        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
            
        if event.type == KEYDOWN and event.key == K_RETURN:
            running = False
             
        if event.type == KEYDOWN and event.key == K_r:
            # Setting up random glyders.
            for i in range(random.randint(10, 20)):
                sx = random.randint(0, MAX_X)
                sy = random.randint(0, MAX_Y)

                if random.randint(0, 1) == 1:
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 0, MAX_Y)] = True;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 1, MAX_Y)] = True;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 2, MAX_Y)] = True;
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 2, MAX_Y)] = True;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 2, MAX_Y)] = True;
                else:
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 0, MAX_Y)] = True;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 1, MAX_Y)] = True;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 2, MAX_Y)] = True;
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 2, MAX_Y)] = True;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 2, MAX_Y)] = True;

            updateDisplay()
                        
        if event.type == MOUSEBUTTONDOWN:
            button_down = True
            button_type = event.button
            
        if event.type == MOUSEBUTTONUP:
            button_down = False
            
        if button_down:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_x = mouse_x / SIZE;
            sp_y = mouse_y / SIZE;

            if button_type == 1:
                board[sp_x][sp_y] = True;
            elif button_type == 3:
                board[sp_x][sp_y] = False;
                
            updateDisplay()


running = True
rand_col = True

while running:
    for event in pygame.event.get():
             
        if event.type == KEYDOWN and event.key == K_b:
            if keep_background == False:
                keep_background = True
            else:
                keep_background = False

        if event.type == QUIT:
                running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
    
    updateDisplay()
    rulesOfLife(board)
    pygame.time.delay(10)