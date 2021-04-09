import pygame
import tkinter as tk
from tkinter import messagebox as msb

from Model.Field import Field
from View.Block import Block
from View.Drawer import Drawer
from View.GameObject import GameObject
import Model.jsonWriter as jw
import pygetwindow as gw
import json
with open("config.json") as f: cfg=json.load(f)

dev=cfg["dev"]

TILE_SIZE = 32

pygame.init()
root = tk.Tk()
root.withdraw()
screen = pygame.display.set_mode(cfg["size"])
game_title = gw.getActiveWindow().title
Block.loadResources()
GameObject.loadResources()

drawer = Drawer(screen, TILE_SIZE)
running = True
clock = pygame.time.Clock()
jw.trimOrder()
order=jw.getOrder()
current_level = 0
field = Field.loadFromFile(f"levels/{order[current_level]}", TILE_SIZE)
drawer.setFieldModel(field)
selected=0
choik=[field.placeBomb,field.placeMine,field.placeQbomb]
# DEATH_TIMER = pygame.USEREVENT + 1
# pygame.time.set_timer(DEATH_TIMER, 0)
dt = 0
death_time = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                field.placeBomb()
            if event.key==pygame.K_c:
                field.placeMine()
            if event.key==pygame.K_v:
                field.placeQbomb()
            if event.key==pygame.K_e:
                choik[selected]()
            if event.key==pygame.K_q:
                selected+=1
                if selected==3:
                    selected=0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        field.movePlayerLeft()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        field.movePlayerRight()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        field.movePlayerUp()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        field.movePlayerDown()

    if keys[pygame.K_1]:
        selected=0
    if keys[pygame.K_2]:
        selected=1
    if keys[pygame.K_3]:
        selected=2

    # Game Mechanic
    state=field.process()
    if state == Field.GAME_STATE_FINISH:
        current_level += 1
        #del field
        field = Field.loadFromFile(f"levels/{order[current_level]}", TILE_SIZE)
        field.reload_level()
        drawer.setFieldModel(field)
        choik = [field.placeBomb, field.placeMine, field.placeQbomb]
    elif state == Field.GAME_STATE_DIED and not dev:
        if death_time == 0:
            death_time = 300
        elif death_time > 100:
            death_time -= dt
        else:
            msb.showwarning(title="You died", message="You died. Continue?")
            win = gw.getWindowsWithTitle(game_title)[0]
            win.activate()
            field.reload_level()
            death_time = 0


    # Drawing
    drawer.clearScreen()
    drawer.drawField()
    drawer.drawInfo(selected)



    dt = clock.tick(60)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()