import numpy as np
import random
import pygame
import sys
import math

#GLOBAL VARIABLES
ROW_COUNT = 9
COLUMN_COUNT = 9
GAMECOUNT = 4;
VALIDCOUNT = GAMECOUNT-1;

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#ADDITIONAL VARIABLES
PLAYER = 0
AI = 1
EMPTY = 0

PLAYER_PIECE = 1
AI_PIECE = 2

game_over = False


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
        for c in range(COLUMN_COUNT-VALIDCOUNT):
                
                count = 0
                for r in range(ROW_COUNT):
                        for x in range(0, GAMECOUNT):
                            if int(board[r][c+x]) != piece:
                                    count = 0
                                    break
                            else:
                                    count += 1
                
                        if (count == GAMECOUNT):
                            return True


        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
                count = 0
                for r in range(ROW_COUNT-VALIDCOUNT):
                        for x in range(0, GAMECOUNT):
                                if board[r+x][c] != piece:
                                        count = 0
                                        break
                                else:
                                        count += 1
                        if (count == GAMECOUNT):
                                return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-VALIDCOUNT):
                count = 0
                for r in range(ROW_COUNT-VALIDCOUNT):
                        for x in range(0, GAMECOUNT):
                                if board[r+x][c+x] != piece:
                                        count = 0
                                        break
                                else:
                                        count += 1
                        if (count == GAMECOUNT):
                                return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-VALIDCOUNT):
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

def evaluate_window(window, piece, wincount):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    
    if window.count(piece) == wincount:
        score += 100
    elif window.count(piece) == wincount-1 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == wincount-2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == wincount-1 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column

    center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    
    ## Score Horizontal
    
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-VALIDCOUNT):
            window = row_array[c:c+GAMECOUNT]           
            score += evaluate_window(window, piece, GAMECOUNT)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-VALIDCOUNT):
            window = col_array[r:r+GAMECOUNT]
            score += evaluate_window(window, piece, GAMECOUNT)

    ## Score positive sloped diagonal
    for r in range(ROW_COUNT-VALIDCOUNT):
        for c in range(COLUMN_COUNT-VALIDCOUNT):
            window = [board[r+i][c+i] for i in range(VALIDCOUNT)]
            score += evaluate_window(window, piece, GAMECOUNT)
            
    ## Score negative sloped diagonal
    for r in range(ROW_COUNT-VALIDCOUNT):
        for c in range(COLUMN_COUNT-VALIDCOUNT):
            window = [board[r+VALIDCOUNT-i][c+i] for i in range(VALIDCOUNT)]
            score += evaluate_window(window, piece, GAMECOUNT)
                
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: #Depth if zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = max(beta, value)
            if alpha >= beta:
                break
        return column, value
    
    

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
    
    
def pick_best_move(board, piece):
    best_score = -10000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        
        if score > best_score:
            best_score = score
            best_col = col
    
    return best_col

def draw_board(board):
        for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):
                        pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                        pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
        for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):              
                        if board[r][c] == PLAYER_PIECE:
                                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                        elif board[r][c] == AI_PIECE: 
                                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()  


turn = random.randint(PLAYER, AI)

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
        pygame.display.update()
                                   
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            #print(event.pos)
            
        
            # Ask for Player 1 Input
            if turn == PLAYER:

                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                

                #Checks if the move is valid
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    #Check winning move
                    if winning_move(board, PLAYER_PIECE):
                        label  = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (100,10))
                        game_over = True

                    print_board(board)
                    draw_board(board)
                

                    turn += 1
                    turn = turn % 2
            
        # AI input
        if turn == AI and not game_over:
            #col = random.randint(0, COLUMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)

            col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
            
            #Checks if the move is valid
            #pygame.time.wait(1000)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            #Check winning move
            if winning_move(board, AI_PIECE):
                label  = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (100,10))
                game_over = True

            #Turn

            print_board(board)
            draw_board(board)
                
            turn += 1
            turn = turn % 2
                

    #Make pygame wait before ending
    if game_over:
        pygame.time.wait(9000)
