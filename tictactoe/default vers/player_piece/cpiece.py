import pygame,sys
import numpy as np
from player_piece.const import *
from board.ultimate_dims import Dimensions

class Piece:
    def __init__(self,symbol,colour):
        self.symbol=symbol # symbol displayed on board, will be a string printed to the board
        self.colour=colour # colour of the symbol

    def draw_symbol(self,screen,row,col,cell_size,ultx,ulty): # draws symbol to screen board 
        #ultx, ulty helps with finding coordinates for squares in ultimate

        self.size=int(0.8*cell_size) # piece size in proportion to square
        self.font=pygame.font.SysFont("segoeui",self.size) # setting font for piece which is text

        self.text=self.font.render(self.symbol,True,self.colour)
        vertical_offset=int(self.size*0.08) # shifting all pieces by a certain value, centres piece
        horizontal_offset=int(self.size*0.014)
        
        x = ultx+ col * cell_size + cell_size // 2
        y = ulty+ row * cell_size + cell_size // 2 # x and y coords for cell centre

        self.rect=self.text.get_rect()
        self.rect.center=(x+horizontal_offset,y-vertical_offset) # sets cell centre, w/ slight adjustments for font type
        screen.blit(self.text,self.rect) # draws image to screen

    def draw_tie(self,screen,x,y,cell_size):
        self.size=int(0.65*cell_size) # piece size in proportion to square
        self.font=pygame.font.SysFont("segoeui",self.size) # setting font for piece which is text

        text=self.font.render(self.symbol,True,self.colour)
        rect=text.get_rect(center=(x,y)) #center freely decided by x,y coords
        screen.blit(text,rect)


