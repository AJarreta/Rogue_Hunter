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
CurrentRedPlayerPosition = copy.deepcopy(RedPlayerStart)
CurrentBluePlayerPosition = copy.deepcopy(BluePlayerStart)
RedStartingMovements = 100
BlueStartingMovements = 100
NumberOfColumns = 19
NumberOfLines = 20

FPS = 30

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
    for Column in range(NumberOfColumns):
        y = 1
        for Line in range(NumberOfLines):
            CurrentSquare = str(x) + ", " + str(y)
            if [x-1, y-1] == BluePosition:
                InputGrid[CurrentSquare] = copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 1
            elif [x-1, y-1] == RedPosition:
                InputGrid[CurrentSquare] = copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 2
            else:
                InputGrid[CurrentSquare] = copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 0
            y += 1
            CurrentPositionA[1] += SquareSize
            CurrentPositionB[1] += SquareSize
        x += 1
        y = 1
        CurrentPositionA[0] += SquareSize
        CurrentPositionB[0] += SquareSize
        CurrentPositionA[1] = copy.deepcopy(StartingPositionA[1])
        CurrentPositionB[1] = copy.deepcopy(StartingPositionB[1])
    GridList = sorted(InputGrid.keys())
    for item in GridList:
       print item, InputGrid[item]

def DrawingGrid(InputGrid, Window, OuterSquareSize, InnerSquareSize, Black, Blue, Red, White):
    x = 1
    y = 1
    for item in range(len(InputGrid)):
        CurrentSquare = str(x) + ", " + str(y)
        if CurrentSquare not in InputGrid.keys():
            x += 1
            y = 1
            CurrentSquare = str(x) + ", " + str(y)
        if InputGrid[CurrentSquare][2] == 1:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, Blue, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        elif InputGrid[CurrentSquare][2] == 2:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, Red, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        else:
            print CurrentSquare, InputGrid[CurrentSquare]
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, White, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        y += 1

def FirstPlayerSelector():
    RandomNumber = random.randint(1, 2)
    if RandomNumber == 1:
        FirstPlayer = "Red"
    else:
        FirstPlayer = "Blue"
    return FirstPlayer



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
InnerSquareSize = int(OuterSquareSize*0.9)
StartingPointA = [int((ScreenWidth - GridWidth) / 2), int((ScreenHeight - GridHeight) / 2)]
StartingPointB = [copy.deepcopy(int(StartingPointA[0] + (OuterSquareSize - InnerSquareSize))),    
                 copy.deepcopy(int(StartingPointA[1] + (OuterSquareSize - InnerSquareSize)))]
global FPSClock, ROGUE_HUNTERWindow
GameStarter = FirstPlayerSelector()

#MAIN LOOP
pygame.init()
FPSClock = pygame.time.Clock()
pygame.display.set_caption('Rogue Hunter')
ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
GridConstructor(PlayingGrid, RedPlayerStart, BluePlayerStart, OuterSquareSize, StartingPointA, StartingPointB)
DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if CurrentBluePlayerPosition[1] > 1:
                    CurrentBluePlayerPosition[1] -= 1
                    GridConstructor(PlayingGrid, RedPlayerStart, CurrentBluePlayerPosition, OuterSquareSize, StartingPointA, StartingPointB)  
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if CurrentBluePlayerPosition[1] < NumberOfLines:
                    CurrentBluePlayerPosition[1] += 1
                    GridConstructor(PlayingGrid, RedPlayerStart, CurrentBluePlayerPosition, OuterSquareSize, StartingPointA, StartingPointB)  
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if CurrentBluePlayerPosition[0] > 1:
                    CurrentBluePlayerPosition[0] -= 1
                    GridConstructor(PlayingGrid, RedPlayerStart, CurrentBluePlayerPosition, OuterSquareSize, StartingPointA, StartingPointB)  
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if CurrentBluePlayerPosition[0] < NumberOfColumns:
                    CurrentBluePlayerPosition[0] += 1
                    GridConstructor(PlayingGrid, RedPlayerStart, CurrentBluePlayerPosition, OuterSquareSize, StartingPointA, StartingPointB)  
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
