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


import pygame
from random import randint
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_r, K_b, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from boxes import Box

MAX_X = 80
MAX_Y = 40
SIZE = 10
keep_background = False
started = False
board = []
screen = False
button_down = False
button_type = False
x = False
y = False
mouse_x = False
mouse_y = False

def borderless(n, t):
    """ Allowing the board to wrap around, "infinite playing field". """

    if n < 0:
        return t + n
    elif n >= t:
        return n - t
    else:
        return n

def updateDisplay():
    for y in range(MAX_Y):
        for x in range(MAX_X):
            if board[x][y]:
                if started:
                    cell = Box([randint(0, 255), randint(0, 255), randint(0, 255)], [x * SIZE, y * SIZE], SIZE)
                else:
                    cell = Box([255, 255, 255], [x * SIZE, y * SIZE], SIZE)
                screen.blit(cell.image, cell.rect)
            elif not keep_background:
                cell = Box([0, 0, 0], [x * SIZE, y * SIZE], SIZE)
                screen.blit(cell.image, cell.rect)
    
    pygame.display.update()

pygame.init()
pygame.display.set_caption('Conway\'s Game of Life by jparmstrong.com')
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])


# Making the board.
board = [False] * MAX_X
    
for i in range(MAX_X):
    board[i] = [False] * MAX_Y

while not started:
    for event in pygame.event.get():

        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
            
        if event.type == KEYDOWN and event.key == K_RETURN:
            started = True
             
        if event.type == KEYDOWN and event.key == K_r:
            # Setting up random glyders.
            for i in range(randint(10, 20)):
                x = randint(0, MAX_X)
                y = randint(0, MAX_Y)

                if randint(0, 1) == 1:
                    board[borderless(x + 1, MAX_X)][borderless(y + 0, MAX_Y)] = True
                    board[borderless(x + 2, MAX_X)][borderless(y + 1, MAX_Y)] = True
                    board[borderless(x + 0, MAX_X)][borderless(y + 2, MAX_Y)] = True
                    board[borderless(x + 1, MAX_X)][borderless(y + 2, MAX_Y)] = True
                    board[borderless(x + 2, MAX_X)][borderless(y + 2, MAX_Y)] = True
                else:
                    board[borderless(x + 1, MAX_X)][borderless(y + 0, MAX_Y)] = True
                    board[borderless(x + 0, MAX_X)][borderless(y + 1, MAX_Y)] = True
                    board[borderless(x + 0, MAX_X)][borderless(y + 2, MAX_Y)] = True
                    board[borderless(x + 1, MAX_X)][borderless(y + 2, MAX_Y)] = True
                    board[borderless(x + 2, MAX_X)][borderless(y + 2, MAX_Y)] = True

            updateDisplay()
                        
        if event.type == MOUSEBUTTONDOWN:
            button_down = True
            button_type = event.button
            
        if event.type == MOUSEBUTTONUP:
            button_down = False
            
        if button_down:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            x = mouse_x / SIZE
            y = mouse_y / SIZE

            if button_type == 1:
                board[x][y] = True
            elif button_type == 3:
                board[x][y] = False
                
            updateDisplay()

while True:
    for event in pygame.event.get():
             
        if event.type == KEYDOWN and event.key == K_b:
            keep_background = keep_background == False

        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
                
    
    updateDisplay()
    pop_list = [0] * MAX_X
    
    for i in range(MAX_X):
        pop_list[i] = [0] * MAX_Y

   # Checking to see what is populated around each cell.
    for y in range(MAX_Y):
        for x in range(MAX_X):
            # row A
            pop_list[x][y] += board[borderless(x-1, MAX_X)][borderless(y-1, MAX_Y)]
            pop_list[x][y] += board[borderless(x, MAX_X)][borderless(y-1, MAX_Y)]
            pop_list[x][y] += board[borderless(x+1, MAX_X)][borderless(y-1, MAX_Y)]
            # row B
            pop_list[x][y] += board[borderless(x-1, MAX_X)][borderless(y, MAX_Y)]
            pop_list[x][y] += board[borderless(x+1, MAX_X)][borderless(y, MAX_Y)]
            # row C
            pop_list[x][y] += board[borderless(x-1, MAX_X)][borderless(y+1, MAX_Y)]
            pop_list[x][y] += board[borderless(x, MAX_X)][borderless(y+1, MAX_Y)]
            pop_list[x][y] += board[borderless(x+1, MAX_X)][borderless(y+1, MAX_Y)]
    
    # Now that we know whats around each cell, we implement the rules of Life.
    for y in range(MAX_Y):
        for x in range(MAX_X):

            if board[x][y] and (pop_list[x][y] < 2 or pop_list[x][y] > 3):
                board[x][y] = False
                
            elif not board[x][y] and pop_list[x][y] == 3:
                board[x][y] = True

    pygame.time.delay(10)