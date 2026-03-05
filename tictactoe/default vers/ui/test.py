import pygame
import sys
from buttons import Buttons
from ui.const import *

pygame.init()
screen=pygame.display.set_mode((600,600))
pygame.display.set_caption("Main Menu")

button_surface=pygame.image.load("button.png")
button_surface=pygame.transform.scale(button_surface,(400,150))

button=Buttons(button_surface,400,300,"PLAY")

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            button.button_clicked(pygame.mouse.get_pos())

    screen.fill(240, 194, 252)

    button.draw_button()

    pygame.display.update()