import sys
import math
import random
import pygame
from pygame.locals import *
import win32api

# FUNCTIONS DEFINITIONS
def GridConstructor(InputGrid):
    for x in range(20):
        GridRow = []
        for x in range(19):
            GridRow.append(0)
        InputGrid.append(GridRow)

# COLOURS DEFINITION
BaseBlack = (0, 0, 0)
BaseWhite = (255, 255, 255)
BaseRed = (255, 0, 0)
BaseBlue = (0, 0, 255)

# CALCULATING THE SIZE OF THE WINDOW AND THE GRID
ScreenWidth = win32api.GetSystemMetrics(0)
ScreenHeight = win32api.GetSystemMetrics(1)
WindowDimensions = [win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]

GridHeight = int(ScreenHeight*0.9)
while (GridHeight % 20) != 0:
    GridHeight -= 1
GridWidth = int(GridHeight*0.95)
BaseSquareSize = GridHeight/20

PlayingGrid = []
GridConstructor(PlayingGrid)
x = 1
for item in PlayingGrid:
    print x, item, '\n'
    x += 1

#MAIN LOOP
pygame.init()
pygame.display.set_caption('Rogue Hunter')
while True:
    ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
    #for item
    pygame.draw.rect(ROGUE_HUNTERWindow, BaseWhite, (BaseSquareSize, BaseSquareSize, BaseSquareSize, BaseSquareSize), 1)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()