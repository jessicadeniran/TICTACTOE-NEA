
from board.const import *

class Dimensions:
    def __init__(self,size,xcoord,ycoord):
        self.size=size
        self.squaresize=size//BOARD_ROWS
        self.x=xcoord
        self.y=ycoord