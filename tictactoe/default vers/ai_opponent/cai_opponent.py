import pygame,sys
import random
import copy
import time
import numpy as np
from ai_opponent.const import *
from board.cboard import Board
from board.const import *
#from game.cgame import Game

class AI_Opponent:
    def __init__(self, difficulty=0, player=2):
        self.difficulty=difficulty # different levels of difficulty for players, e.g. easy,hard
        self.player=player # set to initially be equal to 2 as player in game class is initially equal to 1

    def random_choice(self,board):
        #3x3 board
        if board.ultimate==False:
            empty_sqrs=board.getemptysquares() # list of all available squares
        
        #ultimate
        else:
            empty_sqrs=board.ult_emptysquares() # list of all available squares

        if len(empty_sqrs)!=0: #there are empty squares available - board is not full
            return random.choice(empty_sqrs)
        return None
            
        


    def minimax(self,board,maximising,depth=0): #maximising- bool (true/false)
        '''
        @ returns evaluation (0,1,-1)
        @ returns best move (initially None)
        '''
        #base case
        case=board.final_state() # returns the final state of the board, if case=0, a win hasn't been detected yet
        #player 1 (user) wins
        if case==1:
            return 1, None #maximising
        #player 2 (ai) wins
        if case==2:
            return -1, None #minimising
        #draw
        if board.check_full():
            return 0, None # no winner
        
        if maximising: #simulating user possible moves
            max_eval= -100 #initial value
            best_move= None
            empty_sqrs=board.getemptysquares() # list of empty squares for ai to eval

            for (row,col) in empty_sqrs: # iterate through empty square
                temporaryboard=board.copy() # copy of console board
                temporaryboard.cell_button_clicked(row,col,1) # simulating player move on temp

                eval=self.minimax(temporaryboard,False,depth+1)[0] #first item is eval (0,1,-1), move is (row,col)
                if eval>max_eval: # if eval is a higher value than -100, therefore an optimal move
                    max_eval=eval
                    best_move=(row,col)

            return max_eval,best_move

        elif not maximising: #ai - minimising
            min_eval= 100 # initial value
            best_move= None
            empty_sqrs=board.getemptysquares() # list of empty squares for ai to eval

            for (row,col) in empty_sqrs:
                temporaryboard=board.copy() # copy of console board
                temporaryboard.cell_button_clicked(row,col,2) # ai simulating move on temp

                eval=self.minimax(temporaryboard,True,depth+1)[0] #first item is eval (0,1,-1), move is (row,col)
                if eval<min_eval: #eval is lower value than +100
                    min_eval=eval
                    best_move=(row,col)

            return min_eval,best_move

    def evaluate_board(self,mainboard):
        if mainboard.check_full(): # ai shouldn't make a move if board is full
            return None
        if self.difficulty==0:
            # random
            eval='random'
            move=self.random_choice(mainboard)
            
        elif self.difficulty==2:
            #minimax
            for row, col in mainboard.getemptysquares():
                tempboard=mainboard.copy()
                tempboard.cell_button_clicked(row,col,self.player)
                if tempboard.final_state()==self.player: # if a win is about to occur, ai should try place their piece in that winning place
                    # to either block the user or take the win
                    return row,col
            if mainboard.markedsquares<=1: # first move should be random - lag prevention
                eval=0
                move=self.random_choice(mainboard)
            else: # all other moves should use minimax
                eval,move=self.minimax(mainboard, False)
            
        return move #row,col