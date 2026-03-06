import pygame,sys
import numpy as np
import time
import os
from game.const import *
from board.cboard import Board
from board.const import *
from board.ultimate_dims import Dimensions
from player_piece.const import *
from player_piece.cplayer import Player
from ai_opponent.cai_opponent import AI_Opponent
from ui.buttons import Buttons
#from

class Game:
    def __init__(self):
        self.player=1 # current player is set to 1. this alternates through the switch turn method for players 1 and 2

        self.dims=Dimensions(WIDTH,0,0)
        self.board=Board(dims=self.dims,ultimate=False)
        self.piece_set="default"
        sym1,sym2=PIECE_SET[self.piece_set]
        self.piece1=Player(1).assign_player(sym1,PIECE1_COLOUR)
        self.piece2=Player(2).assign_player(sym2,PIECE2_COLOUR)

        # winning function
        self.game_over=False
        self.winline=None # (win type (str), index, player)
        self.winner=None # value set to winner, set to 0 if draw detected

        # game modes
        self.gamemode = 'ai' #pvp (multiplayer) or ai

        #stats
        self.wins=0
        self.losses=0
        self.total=0

        self.p1wins=0
        self.p2wins=0

        # AI OPPONENT
        self.aiplayer=AI_Opponent()
        self.aithinking=False
        self.aitimer=0

        '''# win timer
        self.showwin=False
        self.wintimer=0'''

        # settings
        self.light=False
        self.sfx_on=True
        self.music_on=True

        #music/sfx
        pygame.mixer.music.load("game/bg music.mp3")

        #clicking
        self.click=pygame.mixer.Sound("game/click sfx.mp3")
        self.click.set_volume(0.83)
        self.gameclick=pygame.mixer.Sound("game/game click.wav")
        self.piececlick=pygame.mixer.Sound("game/piece sfx.mp3")
        self.piececlick.set_volume(0.9)

        #game over/win
        self.ult_sfx=pygame.mixer.Sound("game/ult sfx.mp3") # small board won
        
        self.winsound=pygame.mixer.Sound("game/win sfx.mp3") # wins in sp + mp
        self.losesound=pygame.mixer.Sound("game/lose sfx.mp3") # p1 loss in sp
        self.neutral=pygame.mixer.Sound("game/neutral sfx.mp3") # draws
    
    #extras
    def play_music(self):
        if self.music_on and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        
    def stop_music(self):
        pygame.mixer.music.fadeout(350)

    def win_page_sfx(self,player):
        if self.game_over and self.sfx_on:
            if player==1:
                self.winsound.play()
            if player==2:
                if self.gamemode=="ai":
                    self.losesound.play()
                else:
                    self.winsound.play()
        if self.sfx_on and self.board.markedsquares==9 and self.winline==None:
            self.neutral.play()

    def update_piece(self):
        sym1,sym2=PIECE_SET[self.piece_set]
        self.piece1=Player(1).assign_player(sym1,PIECE1_COLOUR)
        self.piece2=Player(2).assign_player(sym2,PIECE2_COLOUR)

    def switch_turns(self): # ensures that turns alternate between players
        if self.player==1:
            self.player=2
        elif self.player==2:
            self.player=1

    def place_piece(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board.board[row][col]==1:
                    self.piece1.draw_symbol(self.board.screen,row,col,201,0,0)
                elif self.board.board[row][col]==2:
                    self.piece2.draw_symbol(self.board.screen,row,col,201,0,0)
    
    def check_win(self,player):
        #vertical win check
            for col in range(BOARD_COLUMNS):
                if self.board.board[0][col]==player and self.board.board[1][col]==player and self.board.board[2][col]==player:
                    self.winline= ("vertical", col, player)
                    return True
            
        #horizontal win check
            for row in range(BOARD_ROWS):
                if self.board.board[row][0]==player and self.board.board[row][1]==player and self.board.board[row][2]==player:
                    self.winline= ("horizontal", row, player)
                    return True
            
        #ascending diagonal win check
            if self.board.board[2][0]==player and self.board.board[1][1]==player and self.board.board[0][2]==player:
                self.winline= ("asc", None, player)
                return True


        #descending diagonal win check
            if self.board.board[0][0]==player and self.board.board[1][1]==player and self.board.board[2][2]==player:
                self.winline= ("desc", None, player)
                return True
        
            return False

    def draw_winning(self):
        if self.game_over or self.winline!=None: # if game is over or winline has been updated by the win check func
            (wintype, index, player)= self.winline # three values passed in self.wintype attribute once updated
            if wintype == "vertical":
                self.draw_vertical_wl(index, player)
            elif wintype == "horizontal":
                self.draw_horizontal_wl(index, player)
            elif wintype == "asc":
                self.draw_asc_wl(player)
            elif wintype == "desc":
                self.draw_des_wl(player)


    def draw_vertical_wl(self,col,player):
        self.posX=col*201+100
        if player==1:
            self.colour=PIECE1_COLOUR # draws line which is the same colour as the player's piece
        elif player==2:
            self.colour=PIECE2_COLOUR
        
        pygame.draw.line(self.board.screen,self.colour,(self.posX,15),(self.posX,HEIGHT-15),15)

    def draw_horizontal_wl(self,row,player):
        self.posY=row*201+100
        if player==1:
            self.colour=PIECE1_COLOUR # draws line which is the same colour as the player's piece
        elif player==2:
            self.colour=PIECE2_COLOUR
        
        pygame.draw.line(self.board.screen,self.colour,(10,self.posY),(WIDTH-10,self.posY),15)

    def draw_asc_wl(self,player):
        if player==1:
            self.colour=PIECE1_COLOUR
        elif player==2:
            self.colour=PIECE2_COLOUR

        pygame.draw.line(self.board.screen,self.colour,(10,HEIGHT-10),(WIDTH-10,10),15)

    def draw_des_wl(self,player):
        if player==1:
            self.colour=PIECE1_COLOUR
        elif player==2:
            self.colour=PIECE2_COLOUR
            
        pygame.draw.line(self.board.screen,self.colour,(10,10),(WIDTH-10,HEIGHT-10),15)
        
    def restart(self): # resets whole game state
        pygame.display.set_caption("Play")
        self.board.screen.fill(BG_COLOUR)
        self.board.draw_lines()
        self.player=1
        self.game_over=False
        self.winline=None
        self.board.reset()
        self.aiplayer.firstmove=False
        pygame.mixer.stop()

    def ult_restart(self): # reset for ultimate
        pygame.display.set_caption("Play")
        dims=Dimensions(WIDTH,0,0)
        self.board=Board(dims=dims,ultimate=True)
        self.player=1
        self.game_over=False
        self.winline=None
        self.aiplayer.firstmove=False
        pygame.mixer.stop()

    
    def pieces(self):
        self.board.screen.fill((0,0,0))
        while True:
            self.piece1.draw_tie(self.board.screen,150,280,self.dims.size)
            self.piece2.draw_tie(self.board.screen,450,280,self.dims.size)
            self.board.display_window()

#win/loss page
    def win_page(self):
        self.stop_music()
        if self.game_over==True or self.board.markedsquares==9:
            pygame.display.set_caption("Game Over!")
            transparent=pygame.Surface((self.dims.size,self.dims.size))
            transparent.set_alpha(150) #translucent screen
            transparent.fill(BG_COLOUR)
            self.board.screen.blit(transparent,(self.dims.x,self.dims.y))
            
            if self.winline!=None:
                # draws winning piece in centre
                if self.winline[2]==1:
                    winner=1
                    self.piece1.draw_symbol(self.board.screen,self.dims.x,self.dims.y,self.dims.size,0,0)
                if self.winline[2]==2:
                    winner=2
                    self.piece2.draw_symbol(self.board.screen,self.dims.x,self.dims.y,self.dims.size,0,0)

            if self.board.markedsquares==9 and self.winline==None:
                # draw two pieces next to each other
                winner=0
                self.piece1.draw_tie(self.board.screen,150,280,self.dims.size)
                self.piece2.draw_tie(self.board.screen,450,280,self.dims.size)
        

            #win text
            font=pygame.font.SysFont("arialblack",50)
            if winner!=0:
                win_text=(f"PLAYER {winner} HAS WON!")
            else:
                win_text=("DRAW!")
            
            
            win_textobject=font.render(win_text,True,(69, 14, 97))
            rect=win_textobject.get_rect(center=(301,87))
            self.board.screen.blit(win_textobject,rect)

            #instruction text
            i_font=pygame.font.SysFont(None,35)
            ins_text="click 'r' to restart game or click 'h' to go home"
            ins_object=i_font.render(ins_text,True,(69, 14, 97))
            ins_rect=ins_object.get_rect(center=(301,500))
            self.board.screen.blit(ins_object,ins_rect)


    def game_mode(self): #gamemode screen
        pygame.display.set_caption("Choose your Gamemode")
        if self.light:
            bg_image=pygame.image.load("game/light bg.jpg")
        else:
            bg_image=pygame.image.load("game/bg.jpg")
        self.play_music()
        while True:
            self.board.screen.blit(bg_image,(0,0)) #display backgorund imag3e
            mode_mouse_pos=pygame.mouse.get_pos()# used to test if a button is being hovered over/clicked

            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(397,110))
            
            single=Buttons(image=btn_surface,position=(301,310),text="SINGLEPLAYER",colour="white")
            multi=Buttons(image=btn_surface,position=(301,510),text="MULTIPLAYER",colour="white")
            back=Buttons(image=btn_surface,position=(301,110),text="BACK",colour="white")
            
           # draw buttons onto screen
            for button in [single,multi,back]:
                button.change_colour(mode_mouse_pos)
                button.draw_button(self.board.screen)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN: # actions taken if buttons are clicked
                    if single.button_clicked(mode_mouse_pos): # takes user to single page
                        if self.sfx_on:
                            self.gameclick.play()
                        self.gamemode="ai"
                        self.difficulty() 
                    if multi.button_clicked(mode_mouse_pos): # takes user to multi page
                        if self.sfx_on:
                            self.gameclick.play()
                        self.gamemode="pvp"
                        self.multiplayer()
                    if back.button_clicked(mode_mouse_pos): # takes user back to menu
                        if self.sfx_on:
                            self.click.play()
                        self.main_menu()


            
            self.board.display_window() # display page

    def settings(self): #settings page
        pygame.display.set_caption("Settings")
        self.play_music()
        while True:
            if self.light:
                bg_image=pygame.image.load("game/light settings.jpg")
            else:
                bg_image=pygame.image.load("game/settings.jpg")
            self.board.screen.blit(bg_image,(0,0)) # display settings page image
            settings_mouse_pos=pygame.mouse.get_pos()# used to test if a button is being hovered over/clicked

            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(193,55))
            settings_back=Buttons(image=btn_surface,position=(502,570),text="BACK",colour="white") #creating buttons
            

            #piece buttons
            opt1_surface=pygame.image.load("game/button 1.png")
            opt1_surface=pygame.transform.scale(opt1_surface,(90,90))
            opt1=Buttons(image=opt1_surface,position=(370,214),text="",colour="white")

            opt2_surface=pygame.image.load("game/button 2.png")
            opt2_surface=pygame.transform.scale(opt2_surface,(90,90))
            opt2=Buttons(image=opt2_surface,position=(460,214),text="",colour="white")

            opt3_surface=pygame.image.load("game/button 3.png")
            opt3_surface=pygame.transform.scale(opt3_surface,(90,90))
            opt3=Buttons(image=opt3_surface,position=(550,214),text="",colour="white")

            #light/dark mode
            if self.light: # if clicked to set to light
                colour="white"
                light_dark_text="LIGHT"
            else: # if clicked to set to dark
                colour="black"
                light_dark_text="DARK"

            # on/off for music/sfx
            if self.music_on:
                mcolour="green"
                on_text="ON"
                self.play_music()
            else:
                mcolour="red"
                on_text="OFF"
                self.stop_music()
                

            if self.sfx_on:
                scolour="green"
                son_text="ON"
            else:
                scolour="red"
                son_text="OFF"

            #toggle settings buttons
            light_dark=Buttons(image=btn_surface,position=(500,300),text=light_dark_text,colour=colour)
            music=Buttons(image=btn_surface,position=(500,380),text=on_text,colour=mcolour)
            sound=Buttons(image=btn_surface,position=(500,460),text=son_text,colour=scolour)

            #drawing buttons
            for button in [light_dark,music,sound,opt1,opt2,opt3]:
                button.draw_button(self.board.screen)

            for button in [settings_back]:
                button.change_colour(settings_mouse_pos)
                button.draw_button(self.board.screen)


            settings_back.change_colour(settings_mouse_pos)
            settings_back.draw_button(self.board.screen)            

            #toggle buttonsS
                # light/dark
                # on/off for music/sfx

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN: # if buttons are clicked on
                    if settings_back.button_clicked(settings_mouse_pos):
                        if self.sfx_on:
                            self.click.play()
                        self.main_menu()

                    if light_dark.button_clicked(settings_mouse_pos):
                        self.light= not self.light
                        print(self.light)
                    if music.button_clicked(settings_mouse_pos):
                        self.music_on= not self.music_on
                        print(self.music_on)
                    if sound.button_clicked(settings_mouse_pos):
                        self.sfx_on= not self.sfx_on

                    if opt1.button_clicked(settings_mouse_pos):
                        self.piece_set="default"
                        self.update_piece()
                    if opt2.button_clicked(settings_mouse_pos):
                        self.piece_set="option2"
                        self.update_piece()
                    if opt3.button_clicked(settings_mouse_pos):
                        self.piece_set="option3"
                        self.update_piece()

                    for button in [light_dark,music,sound,opt1,opt2,opt3]:
                        if button.button_clicked(settings_mouse_pos) and self.sfx_on:
                            self.click.play()
       

            #highlight piece button
            pieces_dict={
                "default":opt1,
                "option2":opt2,
                "option3":opt3
            }

            selected_set=pieces_dict[self.piece_set]
            for button in [opt1,opt2,opt3]:
                if button==selected_set:
                    x,y=button.rect.center
                    vert_offset=1.6
                    pygame.draw.circle(self.board.screen,"purple",(x,int(y+vert_offset)),38,5) # draw circle around chosen piece set
            self.board.display_window()

    

    def difficulty(self): # difficulty page
        pygame.display.set_caption("Choose your Difficulty")
        if self.light:
            bg_image=pygame.image.load("game/light bg.jpg")
        else:
            bg_image=pygame.image.load("game/bg.jpg")
        self.play_music()
        while True:
            self.board.screen.blit(bg_image,(0,0)) # display bg
            diff_mouse_pos=pygame.mouse.get_pos()# used to test if a button is being hovered over/clicked

            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(290,94))
            #creating buttons
            easy=Buttons(image=btn_surface,position=(301,270),text="EASY",colour="white")           
            medium=Buttons(image=btn_surface,position=(301,390),text="MEDIUM",colour="white")            
            ultimate=Buttons(image=btn_surface,position=(301,510),text="ULTIMATE",colour="white")
            back=Buttons(image=btn_surface,position=(301,110),text="BACK",colour="white")

            # drawing buttons
            for button in [easy,medium,ultimate,back]:
                button.change_colour(diff_mouse_pos)
                button.draw_button(self.board.screen)
                
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN: # buttons being clicked
                    if easy.button_clicked(diff_mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.aiplayer.difficulty=0
                        self.play_game()
                    if medium.button_clicked(diff_mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.aiplayer.difficulty=2
                        self.play_game()
                    if ultimate.button_clicked(diff_mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.running()
                    if back.button_clicked(diff_mouse_pos):
                        if self.sfx_on:
                            self.click.play()
                        self.gamemode=None
                        self.game_mode()

            self.board.display_window()

    def multiplayer(self): # multiplayer page
        pygame.display.set_caption("Choose Standard or Ultimate")
        if self.light:
            bg_image=pygame.image.load("game/light bg.jpg")
        else:
            bg_image=pygame.image.load("game/bg.jpg")
        self.play_music()
        while True:
            self.board.screen.blit(bg_image,(0,0)) # display bg
            mult_mouse_pos=pygame.mouse.get_pos()

            #  on screen button creation
            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(397,110))
            sta=Buttons(image=btn_surface,position=(301,310),text="STANDARD",colour="white")
            ult=Buttons(image=btn_surface,position=(301,510),text="ULTIMATE",colour="white")
            back=Buttons(image=btn_surface,position=(301,110),text="BACK",colour="white")

            for button in [sta,ult,back]:
                button.change_colour(mult_mouse_pos) # colour change if hovered over
                button.draw_button(self.board.screen) # draw button

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN: # button clicked on
                    if sta.button_clicked(mult_mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.play_game() # standard button - 3x3 pvp
                    if ult.button_clicked(mult_mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.running() # ultimate button - ult board pvp
                    if back.button_clicked(mult_mouse_pos):
                        if self.sfx_on:
                            self.click.play()
                        self.gamemode=None 
                        self.game_mode() # previous page
            
            self.board.display_window()


    def play_game(self): # actual 3x3 game page
        pygame.display.set_caption("Play")
        self.stop_music()
        while True:
            self.board.screen.fill(BG_COLOUR) # fill with bg colour 
            self.board.draw_lines() # draw grid lines
            self.place_piece() # allow piece placements to be drawn
            self.draw_winning() # draw winning line if win detected
            self.win_page() # go to win page if end state detected

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                    
                # game
                if event.type==pygame.MOUSEBUTTONDOWN and not self.game_over: #if the user clicks their screen
                    self.mouseX=event.pos[0] #x coordinate
                    self.mouseY=event.pos[1] # y coordinate
                    self.clicked_row=int(self.mouseY//201) # ensures x coord is can only be 0,1, or 2 - reps cells in grid
                    self.clicked_col=int(self.mouseX//201) # ensures y coord is can only be 0,1, or 2 - reps cells in grid
                    if self.board.validate_input(self.clicked_row,self.clicked_col):
                        self.board.cell_button_clicked(self.clicked_row,self.clicked_col,self.player)
                        if self.sfx_on:
                            self.piececlick.play()
                        
                        if self.check_win(self.player): # if win detected
                            self.game_over=True
                            self.win_page_sfx(self.player) 

                            #update multiplayer stats
                            if self.gamemode!="ai":
                                if self.player==1:
                                    self.p1wins+=1
                                if self.player==2:
                                    self.p2wins+=1

                            #update singleplayer stats
                            if self.gamemode=="ai":
                                if self.player==1:
                                    self.wins+=1
                                if self.player==self.aiplayer.player:
                                    self.losses+=1
                                    
                        if self.game_over or self.board.markedsquares==9: # if any end state (win/draw/loss) detected
                            self.total+=1
                            self.win_page_sfx(self.player)

                        if self.game_over==False:
                            self.switch_turns()
                        

                if event.type==pygame.KEYDOWN: # reset board when key is clicked
                    if event.key==pygame.K_r: # key r clicked- reset
                        self.restart()


                    if event.key==pygame.K_b: # key b clicked- back to prvious page from game
                        if self.gamemode=="pvp":
                                if self.winline!=None or self.board.markedsquares==9: # end state detected
                                    self.restart()
                                self.multiplayer()
                                self.gamemode=None
                                
                        if self.gamemode=="ai" and (self.aiplayer.difficulty==0 or self.aiplayer.difficulty==2):
                                if self.winline!=None or self.board.markedsquares==9: # end state detected
                                    self.restart()
                                self.difficulty()
                                
                    if event.key==pygame.K_h: # home button
                        if self.winline!=None or self.board.markedsquares==9:
                            self.restart()
                            self.main_menu()

            if self.gamemode=="ai" and self.player==self.aiplayer.player and not self.game_over:
                if not self.aithinking:
                    self.aithinking=True #ais turn to play, now thinking
                    self.aitimer=pygame.time.get_ticks() # time up until user placed piece
                else:
                    if pygame.time.get_ticks()-self.aitimer>=300: #400ms or more has passed since user's turn
                        # time since program was opened - time before user placed piece
                        move=self.aiplayer.evaluate_board(self.board)
                        if move!=None:
                            row,col=move
                            self.board.cell_button_clicked(row,col,self.player)
                            if self.sfx_on:
                                self.piececlick.play()
                            if self.check_win(self.player): # win detected
                                self.game_over=True
                                self.win_page_sfx(self.player)
                                if self.player==2:
                                    self.losses+=1
                                else:
                                    self.wins += 1
                            if self.game_over or self.board.markedsquares==9:
                                self.total+=1
                                print("sp: ",self.total,self.wins,self.losses)
                            if self.game_over==False:
                                self.switch_turns()
                        
                        self.aithinking=False # set back to false after ai has made their move

            self.board.display_window()
    
    
    def tutorial(self): # tutorial page
        pygame.display.set_caption("Tutorial")
        if self.light:
            bg_image=pygame.image.load("game/light tutorial.jpg")
        else:
            bg_image=pygame.image.load("game/tutorial.jpg")
        self.play_music()
        while True:
            self.board.screen.blit(bg_image,(0,0)) # display tutorial page image
            tut_mouse_pos=pygame.mouse.get_pos()

            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(193,55))
            tut_back=Buttons(image=btn_surface,position=(502,570),text="BACK",colour="white") # place button in bottom corner
            tut_back.change_colour(tut_mouse_pos)
            tut_back.draw_button(self.board.screen)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if tut_back.button_clicked(tut_mouse_pos): # back button
                        if self.sfx_on:
                            self.click.play()
                        self.main_menu()

            self.board.display_window()

    def main_menu(self): # main menu/home page
        pygame.display.set_caption("AI TicTacToe Game! 💜")
        if self.light:
            bg_image=pygame.image.load("game/light background.jpg")
        else:
            bg_image=pygame.image.load("game/background.jpg")
        self.play_music()
        
        while True:
            self.board.screen.blit(bg_image,(0,0))
            mouse_pos=pygame.mouse.get_pos() # used to test if a button is being hovered over/clicked
            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(290,94))
            # creating buttons
            play_button=Buttons(image=btn_surface,position=(301,270),text="PLAY",colour="white")
            tutorial_button=Buttons(image=btn_surface,position=(301,390),text="TUTORIAL",colour="white")
            settings_button=Buttons(image=btn_surface,position=(301,510),text="SETTINGS",colour="white")

            info_surface=pygame.image.load("game/button.png")
            info_surface=pygame.transform.scale(info_surface,(167,55))
            info=Buttons(image=info_surface,position=(91,570),text="info",colour="white")

            for button in [play_button,tutorial_button,settings_button,info]: # drawing buttons + hover colour change
                button.change_colour(mouse_pos)
                button.draw_button(self.board.screen)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN: # button actions

                    for button in [info,tutorial_button,settings_button]:
                        if button.button_clicked(mouse_pos) and self.sfx_on:
                            self.click.play()

                    if play_button.button_clicked(mouse_pos):
                        if self.sfx_on:
                            self.gameclick.play()
                        self.game_mode()
                        #self.play_game()
                    if info.button_clicked(mouse_pos):
                        self.info()
                    if tutorial_button.button_clicked(mouse_pos):
                        self.tutorial()
                    if settings_button.button_clicked(mouse_pos):
                        self.settings()

            self.board.display_window()
            

    def info(self): # information page
        pygame.display.set_caption("Statistics")
        self.play_music()
        if self.light:
            bg_image=pygame.image.load("game/light stats.jpg")
        else:
            bg_image=pygame.image.load("game/stats.jpg")
        while True:
            self.board.screen.blit(bg_image,(0,0)) # display bg
            info_mouse_pos=pygame.mouse.get_pos()

            font=pygame.font.SysFont("arialblack",40)
            if self.light:
                colour=(174, 150, 57)
            else:
                colour=(255, 222, 89)
            total=font.render(str(self.total),True,colour)
            rect=total.get_rect(center=(400,187))
            self.board.screen.blit(total,rect)
          
            yrect=0
            for stat in [self.wins,self.losses]:
                x=font.render(str(stat),True,colour)
                y=x.get_rect(center=(400,(288+yrect)))
                self.board.screen.blit(x,y)
                yrect+=70

            yrect2=0
            for stat in [self.p1wins,self.p2wins]:
                x=font.render(str(stat),True,colour)
                y=x.get_rect(center=(400,(452+yrect2)))
                self.board.screen.blit(x,y)
                yrect2+=70

            btn_surface=pygame.image.load("game/button.png")
            btn_surface=pygame.transform.scale(btn_surface,(193,55))
            info_back=Buttons(image=btn_surface,position=(502,570),text="BACK",colour="white")

            info_back.change_colour(info_mouse_pos)
            info_back.draw_button(self.board.screen)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if info_back.button_clicked(info_mouse_pos):
                        if self.sfx_on:
                            self.click.play()
                        self.main_menu()
            
            self.board.display_window()
    
    def running(self): # actual game for ultimate version
        self.board=Board(dims=self.dims,ultimate=True)
        pygame.display.set_caption("Play")
        self.stop_music()
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type==pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos=event.pos
                    if self.board.ultvalidate(pos[0],pos[1]): # if move received from input is valid
                        self.board.marksquare(pos[0],pos[1],self.player)
                        if self.sfx_on:
                            self.piececlick.play()
                    
                        if self.board.ult_final_state()=="small board": # win detected on smaller board
                            if self.sfx_on:
                                self.ult_sfx.play()
                        self.board.ult_final_state() # final state check
                        if self.check_win(self.player): #win detected on larger board
                            self.game_over=True
                            pygame.mixer.stop()
                            self.win_page_sfx(self.player)
                            if self.gamemode!="ai": # update multiplayer stats
                                if self.player==1:
                                    self.p1wins+=1
                                if self.player==2:
                                    self.p2wins+=1

                            if self.gamemode=="ai": # update singleplayer stats
                                if self.player==1:
                                    self.wins+=1
                                if self.player==self.aiplayer.player:
                                    self.losses+=1

                        if self.game_over or self.board.markedsquares==9: # end state deetcted
                            self.total+=1
                            self.win_page_sfx(self.player)
                        if self.game_over==False:
                                self.switch_turns()
                        
                if event.type==pygame.KEYDOWN: # reset board when key is clicked
                    if event.key==pygame.K_r: # key r clicked- reset
                        self.ult_restart()

                    if event.key==pygame.K_b: # go back a page from ult board
                        if self.gamemode=="ai": # go to difficulty page if ult is ai
                            self.difficulty()
                        else:
                            self.multiplayer() # go to multiplayer page if ult is pvp
                    
                    if event.key==pygame.K_h: # home button clicked, go back to main menu
                        if self.winline!=None or self.board.markedsquares==9:
                            self.ult_restart()
                            self.main_menu()


            if self.gamemode=='ai' and self.player==self.aiplayer.player and not self.game_over: # ai player
                if not self.aithinking:
                    self.aithinking=True
                    self.aitimer=pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks()-self.aitimer>=400: #300ms or more has passed

                        move=self.aiplayer.random_choice(self.board)
                        if move!=None:
                            x,y=move
                            self.board.marksquare(x,y,self.player)
                            if self.sfx_on:
                                self.piececlick.play()

                            if self.board.ult_final_state()=="small board": # win detected on smaller board
                                if self.sfx_on:
                                    self.ult_sfx.play()
                            self.board.ult_final_state()
                            if self.check_win(self.player):
                                self.game_over=True
                                pygame.mixer.stop()
                                self.win_page_sfx(self.player)
                                if self.player==2:
                                    self.losses+=1
                                else:
                                    self.wins += 1
                            if self.game_over or self.board.markedsquares==9:
                                self.total+=1
                                #print(self.total,self.wins,self.losses)
                            if self.game_over==False:
                                self.switch_turns()
                        self.aithinking=False
                
            self.board.screen.fill(BG_COLOUR)
            self.board.render_ultimate(self.board.screen)
            self.board.place_ultpiece(self.piece1,self.piece2)
            self.draw_winning()
            self.win_page()
            self.board.display_window()



