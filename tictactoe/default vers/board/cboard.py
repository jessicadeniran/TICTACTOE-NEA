import pygame,sys
import numpy as np
import random
import copy
from board.const import *
from board.ultimate_dims import Dimensions

class Board:
    def __init__(self,dims,ultimate=False,screen=None):            
       pygame.init() # initialises pygame module
       self.size=(WIDTH,HEIGHT) #screen dimensions
       self.dimensions=(BOARD_ROWS,BOARD_COLUMNS) # tuple which holds grid's dimensions
       self.board=[ [0, 0, 0] for row in range(BOARD_ROWS)] # console board
       self.player=1
       self.markedsquares=0 # number of marked squares
       if not screen:
            self.screen=pygame.display.set_mode(self.size) # displays the board
       else:
           self.screen=screen
       
       # NEW: ULTIMATE TICTACTOE
       self.dims=dims
       self.ultimate=ultimate
       if ultimate:
           self.create_ultimate() # create ultimate board screen
           self.next_board=None # no initial restriction for first move
    

 #DRAWING BOARD METHODS   
    def create_window(self):
        pygame.display.set_caption("AI TicTacToe Game! 💜") # sets the game's caption displayed at the top
        self.screen.fill(BG_COLOUR) # fill background 

    def draw_lines(self): #drawing the lines for the tictactoe grid
    #HORIZONTAL
        pygame.draw.line(self.screen,LINE_COLOUR,(0,201),(603,201),LINE_WIDTH) #values- start and end position of line
        pygame.draw.line(self.screen,LINE_COLOUR,(0,402),(603,402),LINE_WIDTH)

    #VERTICAL
        pygame.draw.line(self.screen,LINE_COLOUR,(201,0),(201,603),LINE_WIDTH)
        pygame.draw.line(self.screen,LINE_COLOUR,(402,0),(402,603),LINE_WIDTH)

 #NEW: ULTIMATE BOARD
    def render_ultimate(self,screen):
        if self.ultimate and self.next_board!=None and self.final_state()==0: #
            row=self.next_board[0]
            col=self.next_board[1]
            highlight_square=self.board[row][col]
            if isinstance(highlight_square,Board):
                pygame.draw.rect(screen,HIGHLIGHT_COLOUR,(highlight_square.dims.x,highlight_square.dims.y,highlight_square.dims.size,highlight_square.dims.size))

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                square=self.board[row][col]

                if isinstance(square,Board): square.render_ultimate(screen)
        if self.ultimate:
            self.linewidth=LINE_WIDTH
        else:
            self.linewidth=SMALL_LINE_WIDTH

        #vertical
        pygame.draw.line(self.screen,LINE_COLOUR,(self.dims.x+self.dims.squaresize,self.dims.y),(self.dims.x+self.dims.squaresize,self.dims.y+self.dims.size),self.linewidth)
        pygame.draw.line(self.screen,LINE_COLOUR,(self.dims.x+self.dims.size-self.dims.squaresize,self.dims.y),(self.dims.x+self.dims.size-self.dims.squaresize,self.dims.y+self.dims.size),self.linewidth)
        #horizontal
        pygame.draw.line(self.screen,LINE_COLOUR,(self.dims.x,self.dims.squaresize+self.dims.y),(self.dims.x+self.dims.size,self.dims.squaresize+self.dims.y),self.linewidth)
        pygame.draw.line(self.screen,LINE_COLOUR,(self.dims.x,self.dims.y+self.dims.size-self.dims.squaresize),(self.dims.x+self.dims.size,self.dims.y+self.dims.size-self.dims.squaresize),self.linewidth)


    def create_ultimate(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
               dims=Dimensions(self.dims.squaresize,self.dims.x+col*self.dims.squaresize,self.dims.x+row*self.dims.squaresize)
               #ultimate=True
               self.board[row][col]=Board(dims,ultimate=False,screen=self.screen)

    def ultvalidate(self,x,y): #validate piece placement for ult
        row=(y-self.dims.y)//self.dims.squaresize
        col=(x-self.dims.x)//self.dims.squaresize

        if (row<0 or row>=3) or (col<0 or col>=3): # row/col validation
            return False
        square=self.board[row][col] # smaller board

        if self.ultimate:
            if (row,col)!=self.next_board and self.next_board!=None: # next board restriction
                return False

        #if 3x3 board
        if not isinstance(square,Board):
            return square==0 # true if empty, false if not
        
        #if ultimate board - recursion
        ultx=x-self.dims.x # x/y coordinates for smaller board in larger board
        ulty=y-self.dims.y
        return square.ultvalidate(ultx,ulty) #recursive- validate piece within smaller board      
          
    def marksquare(self,x,y,player): # ult cell_button_clicked() method
        row=(y-self.dims.y)//self.dims.squaresize
        col=(x-self.dims.x)//self.dims.squaresize
        
        if (row<0 or row>=3) or (col<0 or col>=3): # row/col validation
            return False 
        square=self.board[row][col] # smaller board


        if self.ultimate and self.next_board!=None: # next board has been updated
            if (row,col)!=self.next_board: #small board which != next board
                if isinstance(square,Board):
                    if square.markedsquares==9 or square.final_state()!=0: # board is inactive
                        self.next_board=None #if intended board is inactive, user can play anywhere
                    else:
                        return False
                else:
                    return False # trying to place piece on a won board
                
        if isinstance(square,Board):      
            ultx=x-square.dims.x # x/y coordinates for smaller board in larger board
            ulty=y-square.dims.y

            # coordinates for squares in smaller board
            
            square.marksquare(x,y,player) #recursive piece placement, place piece in smaller board

            #if marked: # if square has been marked
            srow=ulty//square.dims.squaresize #row,col for small board square
            scol=ultx//square.dims.squaresize
            self.update_nextboard(srow,scol) # next board set to row,col of that square
           # return marked #true/false
        
        
        else:
            if square==0:
                self.board[row][col]=player
                self.markedsquares+=1

                if self.ultimate:
                    self.update_nextboard(row,col)
                return True
            return False
        

    def update_nextboard(self,row,col): #row,col for smaller board - method updates next board attribute
        #sets coordinates of next board equal to square that has just been marked
        if (row<0 or row>=3) or (col<0 or col>=3): # validation
            self.next_board=None
            return
        square=self.board[row][col]
        if isinstance(square,Board):
            if square.markedsquares==9 or square.final_state()!=0: # draw/win detected, board is inactive, next player can go anywhere
                self.next_board=None
            else:
                self.next_board=(row,col)
        else:
            self.next_board=None


    def place_ultpiece(self,piece1,piece2):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                square=self.board[row][col]
                if isinstance(square, Board):
                    square.place_ultpiece(piece1,piece2)
                else:
                    if square==1:
                    #pygame.draw.circle(self.board.screen,PIECE1_COLOUR,(int(col*200+200/2),int(row*200+200/2)),CIRC_RADIUS,CIRC_WIDTH)
                        piece1.draw_symbol(self.screen,row,col,self.dims.squaresize,self.dims.x,self.dims.y)
                    elif square==2:
                        piece2.draw_symbol(self.screen,row,col,self.dims.squaresize,self.dims.x,self.dims.y)

    def ult_final_state(self):
        if not self.ultimate:
            return self.final_state() #3x3 board
        
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                square=self.board[row][col]
                if isinstance(square,Board):
                    win=square.ult_final_state() # recursive, ultimate board
                    if win!=0:
                        self.board[row][col]=win # replaces board with winning player num
                        return "small board"

                self.final_state()       

    def ult_emptysquares(self):
        valid_moves=[]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                square=self.board[row][col]
                if isinstance(square,Board):
                    if self.next_board==None or self.next_board==(row,col): # board restriction
                        if square.markedsquares<9 and square.final_state()==0: #board is still active
                            for srow in range(BOARD_ROWS):
                                for scol in range(BOARD_COLUMNS):
                                    if square.board[srow][scol]==0:
                                        x=square.dims.x+scol*square.dims.squaresize+square.dims.squaresize//2
                                        y=square.dims.y+srow*square.dims.squaresize+square.dims.squaresize//2
                                        valid_moves.append((x,y))
        
        return valid_moves
    
#BOARD FUNCTIONALITY METHODS
    def cell_button_clicked(self, row, col, player): #placing a piece, recording it on console board
        self.board[row][col]=player # allows specified player to place their piece where they choose
        self.markedsquares+=1



    def final_state(self):
        '''
        @ returns 0 if there is no win yet, doesn't mean there's a draw
        @ return 1 if player 1 wins
        @ return 2 if player 2 wins
        '''
        #vertical wins
        for col in range(BOARD_COLUMNS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col]!=0:
                return self.board[0][col]
        
        #horizontal wins
        for row in range(BOARD_ROWS):
            if self.board[row][0]== self.board[row][1]== self.board[row][2] and self.board[row][0]!=0:
                return self.board[row][0]
        
        #ascending dia
        if self.board[2][0]== self.board[1][1]== self.board[0][2] and self.board[0][2]!=0:
            return self.board[2][0]

        #descending dia
        if self.board[0][0]== self.board[1][1]== self.board[2][2] and self.board[0][0]!=0:
            return self.board[0][0]
        
        return 0

    def copy(self):
        #temp_board=Board()
        temp_board= Board.__new__(Board)
        temp_board.board=copy.deepcopy(self.board)
        temp_board.markedsquares=self.markedsquares
        return temp_board

#temp_board.markedsquares=self.markedsquares
    def validate_input(self,row,col): #checks if where user is placing their piece is available
        if self.board[row][col]==0:
            return True
        return False
    
    def check_full(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board[row][col]==0:
                    return False
        return True
    
    def check_empty(self,row,col):
        return self.board[row][col]==0
    
    def getemptysquares(self):
        emptysqrs=[]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.check_empty(row,col):
                    emptysqrs.append((row,col))

        return emptysqrs
    

    def reset(self):
       for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                self.board[row][col]=0
       self.markedsquares=0
                


#MAIN METHODS FOR DISPLAYING GAME
    def display_window(self):
        pygame.display.update()

    

#main
#board=Board()
#board.create_window()

#TESTS
#board.cell_button_clicked(0,0,1)
#board.cell_button_clicked(0,2,2)

#print(board.validate_input(0,0))
#board.reset()

#board.run()


