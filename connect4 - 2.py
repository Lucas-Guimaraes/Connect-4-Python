import numpy as np
import pygame
import sys
import math

#GLOBAL VARIABLES
ROW_COUNT = 9
COLUMN_COUNT = 9
GAMECOUNT = 5;

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#ADDITIONAL VARIABLES

game_over = False
turn = 0

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

#Initializes the board
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

#Drops piece onto the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

#Checks if the location is valid to drop in
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

#Gets the next available row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r



#Prints board
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-GAMECOUNT):
		count = 0
		for r in range(ROW_COUNT):
			for x in range(0, GAMECOUNT):
				if board[r][c+x] != piece:
					count = 0
					break
				else:
					count += 1
			if (count == GAMECOUNT):
 				return True


	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		count = 0
		for r in range(ROW_COUNT-GAMECOUNT):
			for x in range(0, GAMECOUNT):
				if board[r+x][c] != piece:
					count = 0
					break
				else:
					count += 1
			if (count == GAMECOUNT):
 				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-GAMECOUNT):
		count = 0
		for r in range(ROW_COUNT-GAMECOUNT):
			for x in range(0, GAMECOUNT):
				if board[r+x][c+x] != piece:
					count = 0
					break
				else:
					count += 1
			if (count == GAMECOUNT):
 				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-GAMECOUNT):
		count = 0
		for r in range(ROW_COUNT):
			for x in range(0, GAMECOUNT):
				if board[r-x][c+x] != piece:
					count = 0
					break
				else:
					count += 1
			if (count == GAMECOUNT):
 				return True


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()  



board = create_board()
print_board(board)
pygame.init()
myfont = pygame.font.SysFont("monospace", 75)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

#Game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
                                   
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            #print(event.pos)
            
        
            # Ask for Player 1 Input
            if turn == 0:

                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                

                #Checks if the move is valid
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    #Check winning move
                    if winning_move(board, 1):
                        label  = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (100,10))
                        game_over = True
            
            # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                
                #Checks if the move is valid
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    #Check winning move
                    if winning_move(board, 2):
                        label  = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (100,10))
                        game_over = True

            #Typical print shenanigans
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

            #Make pygame wait before ending
            if game_over:
                pygame.time.wait(9000)
