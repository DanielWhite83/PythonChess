#####
# Very basic chess board created using the chess library for the chess logic and the pygame library for the GUI
# Click and drag pieces with the mouse
# Created by Daniel White
#
####

import pygame
import os
import sys
import chess

#globals

#time
FPS = 60

#style
WHITE = (255,255,255)
BLACK = (0,0,0)
pygame.font.init()
NOTATION_FONT = pygame.font.SysFont("arial", 15)
BIG_FONT = pygame.font.SysFont("arial", 50)

#dimensions
UNIT = 104
HEIGHT, WIDTH = 104 * 8, 104 * 8


# assets (create a folder called "assets" in the same directory, and fill with these resources)
# pieces and highlight should be same width as UNIT, Board should be same dimensions as HEIGHT and WIDTH
ASSETS = {
  "r": pygame.image.load(os.path.join('assets', 'br.png')), # black rook
  "n": pygame.image.load(os.path.join('assets', 'bn.png')), # black knight
  "b": pygame.image.load(os.path.join('assets', 'bb.png')), # black bishop
  "q": pygame.image.load(os.path.join('assets', 'bq.png')), # black queen
  "k": pygame.image.load(os.path.join('assets', 'bk.png')), # black king
  "p": pygame.image.load(os.path.join('assets', 'bp.png')), # black pawn
  "R": pygame.image.load(os.path.join('assets', 'wr.png')), # white rook
  "N": pygame.image.load(os.path.join('assets', 'wn.png')), # white knight
  "B": pygame.image.load(os.path.join('assets', 'wb.png')), # white bishop
  "Q": pygame.image.load(os.path.join('assets', 'wq.png')), # white queen
  "K": pygame.image.load(os.path.join('assets', 'wk.png')), # white king
  "P": pygame.image.load(os.path.join('assets', 'wp.png')), # white pawn
  "board": pygame.image.load(os.path.join('assets', 'board.png')), # chessboard
  "highlight": pygame.image.load(os.path.join('assets', 'highlight.png')) # highlight (png square with 25% opacity)
}

# initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Chessboard by Dan White")
clock = pygame.time.Clock()

def main():

    move = (False, False)
    drag = False
    
    #toggle this variable to flip the board
    flip = False

    close_window_delay = 0

    board = chess.Board()
   
    # game loop
    run = True
    while run:
        #ticking
        clock.tick(FPS)
        
        #event handler
        for event in pygame.event.get():

            # when the mouse is held down
            if event.type == pygame.MOUSEBUTTONDOWN:
                move = (GetMove(pygame.mouse.get_pos()), move[1])
                drag = True

            # when the mouse is released    
            elif event.type == pygame.MOUSEBUTTONUP:
                move = (move[0], GetMove(pygame.mouse.get_pos()))
                TryMove(board, move, flip)
                drag = False

            #draw the board
            DrawBoard(board, move, flip, drag)

            # the game is finished
            ending = TestForEnding(board)
            if ending != False:                
                label = BIG_FONT.render(ending, True, BLACK)
                WIN.blit(label, (100, HEIGHT/3))
                pygame.display.update()


            # if exit button is pressed
            if event.type == pygame.QUIT:
                run = False
                
    pygame.quit()
    sys.exit(0)


# Check for game ending parameters
def TestForEnding(board):
    if board.is_fivefold_repetition():
        return "Game drawn by fivefold repetition."
        
    if board.is_seventyfive_moves():
        return "Game drawn by seventy-five move rule."
        
    if board.is_stalemate():
        return "Game drawn by stalemate."
        
    if board.is_insufficient_material():
        return "Game drawn by insufficient material."
        
    if board.is_checkmate():
        if board.turn:
            winner = "Black"
        else:
            winner = "White"

        return "Checkmate {} Wins.".format(winner)
        
    return False

#convert the mouse position into grid coordinates
#(0,0) is upper left, (7,7) is lower right
def GetMove(move):  
    move = (int(move[0]/UNIT), int(move[1]/UNIT))
    return move


#attempt to play the move on the board
def TryMove(board, move, flip = False):

    # move comes in as a tuple of tuples (4 integers)
    # break the move into 4 pieces
    # the move notation has to be changed depending on if the board is flipped
    if flip:
        from_file = chr(104-move[0][0])
        from_rank = str(1+move[0][1])
        to_file = chr(104-move[1][0])
        to_rank = str(1+move[1][1])
    else:
        from_file = chr(97+move[0][0])
        from_rank = str(8-move[0][1])
        to_file = chr(97+move[1][0])
        to_rank = str(8-move[1][1])

    # attempt to play the move


    try:
        #first check if it is even considered a move
        full_move = chess.Move.from_uci(from_file+from_rank+to_file+to_rank)

        # second see if the the move is legal
        if full_move in board.legal_moves:
            # if the move is legal, then play the move and return True
            san = board.san(full_move)
            board.push(full_move)
            print("Move: {} Alg: {}".format(full_move, san))
            return True
        else:
            # if the move isn't legal, return False
            return False
    except:
        # if the move cannot be played for any reason, return False
        return False
    

def DrawBoard(board, move, flip=False, drag=False):

    # reset a board
    WIN.fill(WHITE)
    WIN.blit(ASSETS['board'],(0,0))

    # process the current state of the board
    processed_board = board.fen().split(" ")
    processed_board = processed_board[0].split("/")

    
    # handle the flipped board
    if flip:
        tmp_board = []
        for i in reversed(processed_board):  
            tmp_board.append(i[::-1])
        processed_board = tmp_board
        # range for ranks and files (if flipped, files are h-a, ranks are 8-1)
        
        file_range = range(1,9)
        rank_range = range(104, 96, -1)
    else:
        # range for ranks and files (if normal, files are a-h, ranks are 1-8)
        file_range = range(8,0,-1)
        rank_range = range(97, 105)

    #highlight the previous move
    if len(board.move_stack) > 0:
        #gets string of most recent move
        cur_move = board.move_stack[-1].uci()
        x0 = ord(cur_move[:1])-97
        y0 = 8-int(cur_move[1:2])
        x1 = ord(cur_move[2:3])-97
        y1 = 8-int(cur_move[3:])
        # invert the coordinates if the board is flipped
        if flip:
            x0 = 7-x0
            y0 = 7-y0
            x1 = 7-x1
            y1 = 7-y1
            
            WIN.blit(ASSETS['highlight'],(x0*UNIT,y0*UNIT))
            WIN.blit(ASSETS['highlight'],(x1*UNIT,y1*UNIT))
            
            
    
    #print notation
    counter = 0
    for i in rank_range:
        label = NOTATION_FONT.render(chr(i), True, BLACK)
        WIN.blit(label, ((counter+1)*UNIT-10, UNIT*8-15))
        counter = counter + 1
    
    counter = 0
    for i in file_range:
        label = NOTATION_FONT.render(str(i), True, BLACK)
        WIN.blit(label, (5, counter*UNIT+5))
        counter = counter + 1        

    # initialize the drag_piece
    # should not be necessary, but there are some timing issues where lacking this can cause an error
    drag_piece = False

    # place the pieces on the board
    x, y = 0 , 0
    for i in processed_board:
        for j in i:
            if j.isnumeric():
                for k in range(int(j)):
                    x = x + 1
            else:
                # if the piece is the one being dragged, don't display it
                # also set the variable with the piece type for later
                if drag and x == move[0][0] and y == move[0][1]:
                    drag_piece = j
                    pass
                else:
                    WIN.blit(ASSETS[j], (x*UNIT, y*UNIT))
                # move to the rank to the right
                x = x + 1
                
        #reset the rank to the far left and move the rank down
        x = 0
        y = y + 1       

    # if there is a piece being dragged, place the image on the mouse cursor
    if drag and drag_piece != False:
        #UNIT/2 places the piece in the middle of the cursor rather than to the bottom right
        x = pygame.mouse.get_pos()[0] - UNIT/2
        y = pygame.mouse.get_pos()[1] - UNIT/2
        WIN.blit(ASSETS[drag_piece], (x,y))

    # update the display with the new images    
    pygame.display.update()
    pass

# run the main function automatically
if __name__ == "__main__":
    main()
