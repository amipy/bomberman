import os

import pygame

from Model.Field import Field
from View.Block import Block
from View.Drawer import Drawer
from View.GameObject import GameObject
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import Model.jsonWriter as jw
#from Model.jsonWriter import *

TILE_SIZE = 32

def save_level():
    filename = filedialog.asksaveasfilename()
    short_f_name = os.path.basename(filename)#filename.split('/')[-1]
    Field.saveFieldToFile(field, filename)
    answer = simpledialog.askinteger("Level number", "What number level is this?")
    levels=jw.getOrder(short_f_name)
    if answer>len(levels):
        answer=len(levels)

    levels.insert(answer-1, short_f_name)
    jw.setOrder(levels) # длинношеее
    jw.trimOrder()
    #print("File saved successfully")

root = tk.Tk()
root.withdraw()
pygame.init()
screen = pygame.display.set_mode([800, 600])
Block.loadResources()
GameObject.loadResources()

width = 20#int(input("Enter width: "))
height = 10#int(input("Enter height: "))
field = Field.createEmptyField(width, height)

drawer = Drawer(screen, TILE_SIZE)
drawer.setFieldModel(field)
running = True
clock = pygame.time.Clock()

while running:

    # INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                field.moveCellForEditRight()
            if event.key==pygame.K_LEFT:
                field.moveCellForEditLeft()
            if event.key==pygame.K_UP:
                field.moveCellForEditUp()
            if event.key==pygame.K_DOWN:
                field.moveCellForEditDown()
            if event.key==pygame.K_COMMA:
                field.changeCell(-1)
            if event.key==pygame.K_PERIOD:
                field.changeCell(1)
            if event.key== pygame.K_s:
                save_level()

    # Drawing
    drawer.clearScreen()
    drawer.drawFieldForEdit()
    drawer.drawInfoForEdit()



    clock.tick(60)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()