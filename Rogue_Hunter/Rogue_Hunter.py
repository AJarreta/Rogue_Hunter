import sys
import math
import random
import pygame
from pygame.locals import *
import win32api

# GENERAL VARIABLES
WindowDimensions = [0, 0]
GridDimensions = [0, 0]
PlayingGrid = []
RedPlayerStart = [9, 4]
BluePlayerStart = [9, 15 ]

# FUNCTIONS DEFINITIONS
def GridConstructor(InputGrid, RedPosition, BluePosition):
    PositionMarker = [0, 0]
    for x in range(20):
        PositionMarker[0] = x
        GridRow = []
        for y in range(19):
            PositionMarker[1] = y
            if PositionMarker == RedPosition:
                GridRow.append(1)
            elif PositionMarker == BluePosition:
                GridRow.append(2)
            else:
                GridRow.append(0)
            InputGrid.append(GridRow)

def GridUpdate(InputGrid, RedPosition, BluePosition):
    PositionMarker = [0, 0]
    for x in len(InputGrid[x]):
        PositionMarker[0] = x
        GridRow = []
        for y in range(19):
            PositionMarker[1] = y
            if PositionMarker == RedPosition:
                GridRow[x][y] = 1
            elif PositionMarker == BluePosition:
                GridRow[x][y] = 2
            else:
                GridRow[x][y] = 0

def DrawingGrid(InputGrid, Surface, GridDimensions, WindowDimensions, SquareSize):
    StartingPositionA = [int((WindowDimensions[0] - GridDimensions[0])/2), int((WindowDimensions[1] - GridDimensions[1])/2)]
    StartingPositionB = [int(StartingPositionA[0] * 1.05), int(StartingPositionA[1] * 1.05)]
    CurrentPositionA = StartingPositionA
    CurrentPositionB = StartingPositionB
    for x in InputGrid:
        index = 0
        for y in InputGrid[index]:
            if y == 0:
                pygame.draw.rect(Surface, BaseBlack, (CurrentPositionA[0], CurrentPositionA[1], SquareSize, SquareSize), 0)
                pygame.draw.rect(Surface, BaseWhite, (CurrentPositionB[0], CurrentPositionB[1], int(SquareSize * 0.9), int(SquareSize * 0.9)), 0)
                CurrentPositionA[1] += SquareSize
                CurrentPositionB[1] += SquareSize
                print InputGrid[index][y]
                print StartingPositionA
                print StartingPositionB
            elif y == 1:
                pygame.draw.rect(Surface, BaseBlack, (CurrentPositionA[0], CurrentPositionA[1], SquareSize, SquareSize), 0)
                pygame.draw.rect(Surface, BaseRed, (CurrentPositionB[0], CurrentPositionB[1], int(SquareSize * 0.9), int(SquareSize * 0.9)), 0)
                CurrentPositionA[1] += SquareSize
                CurrentPositionB[1] += SquareSize
            else:
                pygame.draw.rect(Surface, BaseBlack, (CurrentPositionA[0], CurrentPositionA[1], SquareSize, SquareSize), 0)
                pygame.draw.rect(Surface, BaseBlue, (CurrentPositionA[0], CurrentPositionB[1], int(SquareSize * 0.9), int(SquareSize * 0.9)), 0)
                CurrentPositionA[1] += SquareSize
                CurrentPositionB[1] += SquareSize
        CurrentPositionA[0] += SquareSize
        CurrentPositionA[1] = StartingPositionA
        CurrentPositionB[0] += SquareSize
        CurrentPositionB[1] = StartingPositionB
        index +=1

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
GridDimensions = [GridWidth, GridWidth]
BaseSquareSize = GridHeight/20

'''GridConstructor(PlayingGrid)
x = 1
for item in PlayingGrid:
    print x, item, '\n'
    x += 1'''

#MAIN LOOP
pygame.init()
pygame.display.set_caption('Rogue Hunter')
while True:
    ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
    GridConstructor(PlayingGrid, RedPlayerStart, BluePlayerStart)
    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, GridDimensions, WindowDimensions, BaseSquareSize)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()