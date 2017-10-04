import sys
import math
import random
import pygame
from pygame.locals import *
import win32api
import copy

# GENERAL VARIABLES
WindowDimensions = [0, 0]
GridDimensions = [0, 0]
PlayingGrid = {}
RedPlayerStart = [9, 4]
BluePlayerStart = [9, 15 ]
RedStartingMovements = 100
BlueStartingMovements = 100

# COLOURS DEFINITION
BaseBlack = (0, 0, 0)
BaseWhite = (255, 255, 255)
BaseRed = (255, 0, 0)
BaseBlue = (0, 0, 255)

# FUNCTIONS DEFINITIONS
def GridConstructor(InputGrid, RedPosition, BluePosition, SquareSize, StartingPositionA, StartingPositionB):
    CurrentPositionA = copy.deepcopy(StartingPositionA)
    CurrentPositionB = copy.deepcopy(StartingPositionB)
    x = 1
    for Line in range(19):
        y = 1
        for Row in range(18):
            if [y, x] == BluePosition:
                InputGrid[str(x) + ", " + str(y)] = [CurrentPositionA], [CurrentPositionB], 1
                print CurrentPositionA, CurrentPositionB
            elif [y, x] == RedPosition:
                InputGrid[str(x) + ", " + str(y)] = [CurrentPositionA], [CurrentPositionB], 2
                print CurrentPositionA, CurrentPositionB
            else:
                InputGrid[str(x) + ", " + str(y)] = [CurrentPositionA], [CurrentPositionB], 0
                print CurrentPositionA, CurrentPositionB
            y += 1
            CurrentPositionA[1] += SquareSize
            CurrentPositionB[1] += SquareSize
        x += 1
        CurrentPositionA[0] += SquareSize
        CurrentPositionB[0] += SquareSize
        CurrentPositionA[1] = StartingPositionA[1]
        CurrentPositionB[1] = StartingPositionB[1]

def DrawingGrid(InputGrid, Window, OuterSquareSize, InnerSquareSize, Black, Blue, Red, White):
    x = 1
    y = 1
    for item in range(len(InputGrid)):
        CurrentSquare = str(x) + ", " + str(y)
        if CurrentSquare not in InputGrid.keys():
            x += 1
            y = 1
            CurrentSquare = str(x, ", ", y)
        if InputGrid[CurrentSquare][2] == 1:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, SquareSize), 0)
            pygame.draw.rect(Window, Blue, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, SquareSize), 0)
        elif InputGrid[CurrentSquare][2] == 2:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, SquareSize), 0)
            pygame.draw.rect(Window, Red, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, SquareSize), 0)
        else:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, SquareSize), 0)
            pygame.draw.rect(Window, White, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, SquareSize), 0)



# CALCULATING THE SIZE OF THE WINDOW AND THE ONSCREEN ELEMENTS
ScreenWidth = win32api.GetSystemMetrics(0)
ScreenHeight = win32api.GetSystemMetrics(1)
WindowDimensions = [win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]
GridHeight = int(ScreenHeight*0.9)
while (GridHeight % 20) != 0:
    GridHeight -= 1
GridWidth = int(GridHeight*0.95)
GridDimensions = [GridWidth, GridHeight]
OuterSquareSize = GridHeight/20
InnerSquareSize = OuterSquareSize*0.9
print ScreenHeight, ScreenWidth, GridHeight, GridWidth, GridDimensions, OuterSquareSize, InnerSquareSize, "\n"

x = 1
for item in PlayingGrid:
    print x, item, '\n'
    x += 1

#MAIN LOOP
pygame.init()
pygame.display.set_caption('Rogue Hunter')
while True:
    ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
    GridConstructor(PlayingGrid, RedPlayerStart, BluePlayerStart, OuterSquareSize, [0,  0], [4, 4])
    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, OuterSquareSize, InnerSquareSize, BaseBlue, BaseRed, BaseWhite)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()