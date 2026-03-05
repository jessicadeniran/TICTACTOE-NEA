import pygame,sys
import numpy as np
from player_piece.const import *
from player_piece.cpiece import Piece

class Player:
    def __init__(self,player_num): 
        self.p_num=player_num #corresponds to player 1 and player 2, identifies the player
        self.piece=None #empty attribute, so that piece can be assigned to player in a different method
        self.current_score=0 # will increment by 1 for each win, will be done after creating winning function

        pass

    def assign_player(self,symbol,colour):
        self.piece=Piece(symbol,colour)
        return self.piece # returns the player's piece based on their number
        
    #def add_score():

