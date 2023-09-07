import sys
import numpy as np
from scipy.signal import convolve2d
import pygame
import math


ROWS = 6
COLUMNS = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def make_board():
    board = np.zeros((ROWS, COLUMNS))
    return board


def drop_piece_on_board(board, row, col, piece):
    board[row][col] = piece


def is_valid(board, col):
    return board[0][col] == 0


def get_next_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


def winning_move(board):
    for kernel in detection_kernels:
        if (convolve2d(board, kernel, mode="valid") == 4).any():
            return True
    return False


def draw_board(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2,
                                   r * SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE/2,
                                   r * SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE/2,
                                   r * SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)
    pygame.display.update()


horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel,
                     vertical_kernel, diag1_kernel, diag2_kernel]

board = make_board()
print(board)
gameover = False
turn = 0

pygame.init()

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not gameover:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn % 2 == 0:
                pygame.draw.circle(screen, RED, (posx, SQUARESIZE/2), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, SQUARESIZE/2), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            valid = False
            # Player 1
            if turn % 2 == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid(board, col):
                    row = get_next_row(board, col)
                    drop_piece_on_board(board, row, col, 1)
                    print("Player 2's turn")
                    draw_board(board)
                    valid = True

                new_board = board.copy()
                np.place(new_board, new_board == 2, 0)
                if winning_move(new_board):
                    print("Player 1 wins!")
                    label = myfont.render("Player 1 wins!", 1, RED)
                    screen.blit(label, (40, 10))
                    gameover = True
                    pygame.display.update()

            # Player 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid(board, col):
                    row = get_next_row(board, col)
                    drop_piece_on_board(board, row, col, 2)
                    print("Player 1's turn")
                    draw_board(board)
                    valid = True

                new_board = board.copy()
                np.place(new_board, new_board == 1, 0)
                np.place(new_board, new_board == 2, 1)
                if winning_move(new_board):
                    print("Player 2 wins!")
                    label = myfont.render("Player 2 wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    gameover = True
                    pygame.display.update()

            if valid:
                turn += 1

            if gameover:
                pygame.time.wait(5000)
