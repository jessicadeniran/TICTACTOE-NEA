import pygame
import sys
import os
from ui.const import *


class Buttons:
    def __init__(self,image,position,text,colour):#,action):
        self.colour=colour
        self.font=pygame.font.SysFont("arialblack",40)
        self.image=image
        self.rect=self.image.get_rect(center=(position))
        self.text=text
        self.textobject=self.font.render(self.text,True,self.colour)
        self.textrect=self.textobject.get_rect(center=(position[0],(position[1]-7.35)))
        #self.action=action
        #self.visible=False

    def draw_button(self,screen):
        screen.blit(self.image,self.rect) # puts button on screen
        screen.blit(self.textobject,self.textrect) # puts button text on screen
    
    def button_clicked(self,position): 
        return self.rect.collidepoint(position) # returns true if button was clicked
           
    
    def change_colour(self,position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            self.textobject=self.font.render(self.text,True,(200,200,200))
        else:
            self.textobject=self.font.render(self.text,True,self.colour)
        #pass# hovering over button

#button_surface=pygame.image.load("button.png")
'''button_surface=pygame.transform.scale('''

