
from board.const import *

class Dimensions:
    def __init__(self,size,xcoord,ycoord):
        self.size=size # screen size
        self.squaresize=size//BOARD_ROWS # size of each square within boatf
        self.x=xcoord # x/y coord of square
        self.y=ycoord
