import sys
import math
import random
import pygame
from pygame.locals import *
import win32api
import copy

# FUNCTIONS DEFINITIONS
def GridConstructor(RedPosition, BluePosition, SquareSize, StartingPositionA, StartingPositionB):
    InputGrid = {}
    CurrentPositionA = copy.deepcopy(StartingPositionA)
    CurrentPositionB = copy.deepcopy(StartingPositionB)
    x = 0
    for Column in range(NumberOfColumns):
        y = 0
        for Line in range(NumberOfLines):
            CurrentSquare = "[" + str(x) + ", " + str(y) + "]"
            if [x, y] == BluePosition:
                InputGrid[CurrentSquare] = [copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 1]
            elif [x, y] == RedPosition:
                InputGrid[CurrentSquare] = [copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 2]
            else:
                InputGrid[CurrentSquare] = [copy.deepcopy(CurrentPositionA), copy.deepcopy(CurrentPositionB), 0]
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
    return InputGrid

def DrawingGrid(InputGrid, Window, OuterSquareSize, InnerSquareSize, Black, Blue, Red, White):
    x = 0
    y = 0
    for item in range(len(InputGrid)):
        CurrentSquare = "[" + str(x) + ", " + str(y) + "]"
        if CurrentSquare not in InputGrid.keys():
            x += 1
            y = 0
            CurrentSquare = "[" + str(x) + ", " + str(y) + "]"
        if InputGrid[CurrentSquare][2] == 1:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, Blue, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        elif InputGrid[CurrentSquare][2] == 2:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, Red, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        else:
            pygame.draw.rect(Window, Black, (InputGrid[CurrentSquare][0][0], InputGrid[CurrentSquare][0][1], OuterSquareSize, OuterSquareSize), 0)
            pygame.draw.rect(Window, White, (InputGrid[CurrentSquare][1][0], InputGrid[CurrentSquare][1][1], InnerSquareSize, InnerSquareSize), 0)
        y += 1
    pygame.display.update()

def FirstPlayerSelector():
    RandomNumber = random.randint(1, 2)
    if RandomNumber == 1:
        FirstPlayer = "Red"
    else:
        FirstPlayer = "Blue"
    return FirstPlayer

def GameOver(Window, TextFont, CurrentPlayer, Blue, Red):
    ScreenWidth = Window.get_width()
    ScreenHeight = Window.get_height()
    if CurrentPlayer == 'Blue':
        CurrentPlayerColour = Blue
    else:
        CurrentPlayerColour = Red
    FirstGameOverLine = TextFont.render('Game Over! ' + CurrentPlayer + ' Player is the winner', False, CurrentPlayerColour)
    TextWidth = FirstGameOverLine.get_width()
    TextHeight = FirstGameOverLine.get_height()
    FirstLinePosition = ((ScreenWidth - TextWidth) / 2, (ScreenHeight / 2) - (TextHeight - 2))
    Window.blit(FirstGameOverLine, FirstLinePosition)
    SecondGameOverLine = TextFont.render('Press a key to continue', False, BaseRed)
    TextWidth = SecondGameOverLine.get_width()
    TextHeight = SecondGameOverLine.get_height()
    SecondLinePosition = ((ScreenWidth - TextWidth) / 2, (ScreenHeight / 2) + (TextHeight + 2))
    Window.blit(SecondGameOverLine, SecondLinePosition)
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            Quit()

def TurnChange(Window, TextFont, CurrentPlayer, Blue, Red):
    ScreenWidth = Window.get_width()
    ScreenHeight = Window.get_height()
    if CurrentPlayer == 'Blue':
        CurrentPlayerColour = Blue
    else:
        CurrentPlayerColour = Red
    TurnChangeText = TextFont.render(CurrentPlayer + " Player Turn", False, CurrentPlayerColour)
    TextWidth = TurnChangeText.get_width()
    TextHeight = TurnChangeText.get_height()
    TextPosition = ((ScreenWidth - TextWidth) / 2, (ScreenHeight / 2) - (TextHeight / 2))
    Window.blit(TurnChangeText, TextPosition)
    pygame.display.update()

def DrawMovements(Window, GridDimensions, TextFont, BluePlayerMovements, RedPlayerMovements, Blue, Red, Black):
    BluePlayerScoreText = TextFont.render(str(BluePlayerMovements), False, Blue)
    RedPlayerScoreText = TextFont.render(str(RedPlayerMovements), False, Red)
    BlueScoreWidth = BluePlayerScoreText.get_width()
    RedScoreWidth = RedPlayerScoreText.get_width()
    ScreenWidth = Window.get_width()
    ScreenHeight = Window.get_height()
    ScreenPadding = (ScreenWidth - GridDimensions[0]) / 2
    BlueScoreXPosition = (ScreenPadding - BlueScoreWidth) / 2
    RedScoreXPosition = (ScreenPadding + GridDimensions[0]) + ((ScreenPadding - RedScoreWidth) / 2)
    TextHeight = BluePlayerScoreText.get_height()
    ScoreYPosition = (ScreenHeight / 2) - (TextHeight / 2)
    BlackRectangleWidth = ScreenPadding / 2
    LeftBlackRectangleXPosition = (ScreenPadding - BlackRectangleWidth) / 2
    RightBlackRectangleXPosition = (ScreenPadding + GridDimensions[0]) + ((ScreenPadding - BlackRectangleWidth) / 2)
    pygame.draw.rect(Window, Black, (LeftBlackRectangleXPosition, ScoreYPosition, BlackRectangleWidth, TextHeight), 0)
    Window.blit(BluePlayerScoreText, (BlueScoreXPosition, ScoreYPosition))
    pygame.draw.rect(Window, Black, (RightBlackRectangleXPosition, ScoreYPosition, BlackRectangleWidth, TextHeight), 0)
    Window.blit(RedPlayerScoreText, (RedScoreXPosition, ScoreYPosition))
    pygame.display.update()

def GameTitle(Window, WindowDimensions, TextFont, White):
    Title = TextFont.render("ROGUE HUNTER", False, White)
    TextWidth = Title.get_width()
    TextHeight = Title.get_height()
    TitleXPosition = (WindowDimensions[0] - TextWidth) / 2
    TitleYPosition = (WindowDimensions[1] / 2) - (TextHeight / 2)
    Window.blit(Title, (TitleXPosition, TitleYPosition))
    pygame.display.update()
    Switch = True
    while Switch == True:
        pygame.event.clear()
        pygame.event.wait()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                Switch = False
    

def Quit():
    pygame.quit()
    sys.exit()

#MAIN LOOP
def main():
    pygame.init()
    pygame.font.init()
    PlainTextFont = pygame.font.SysFont('visitortt1brk', 50)
    HeaderFont = pygame.font.SysFont('visitortt1brk', 75)
    NumberFont = pygame. font.SysFont('visitortt1brk', 100)
    TitleFont = pygame.font.SysFont('visitortt1brk', 150)
    FPSClock = pygame.time.Clock()
    CurrentPlayer = FirstPlayerSelector()
    RedMovements = 100
    BlueMovements = 100
    CurrentTurnMovements = 0
    NextTurnSwitch = False
    pygame.display.set_caption('Rogue Hunter')
    ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
    GameTitle(ROGUE_HUNTERWindow, WindowDimensions, TitleFont, BaseWhite) 
    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
    DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
    while True:
        if CurrentPlayer == 'Blue':
            TurnChange(ROGUE_HUNTERWindow, PlainTextFont, CurrentPlayer, BaseBlue, BaseRed)
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        Quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Quit()
                        elif event.key == pygame.K_f:
                            ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions, pygame.FULLSCREEN)
                        elif event.key == pygame.K_RETURN:
                            NextTurnSwitch = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if CurrentBluePlayerPosition[1] > 0:
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[1] -= 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentBluePlayerPosition[1] < (NumberOfLines - 1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[1] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentBluePlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NumberOfColumns-1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                if CurrentTurnMovements == MaxMovements or NextTurnSwitch == True:
                    CurrentPlayer = 'Red'
                    NextTurnSwitch = False
                    CurrentTurnMovements = 0
                    break
                if CurrentBluePlayerPosition == CurrentRedPlayerPosition:
                    GameOver(ROGUE_HUNTERWindow, PlainTextFont, CurrentPlayer, BaseBlue, BaseRed)
                    pygame.event.clear()
                    pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        Quit()
        elif CurrentPlayer == 'Red':
            TurnChange(ROGUE_HUNTERWindow, PlainTextFont, CurrentPlayer, BaseBlue, BaseRed)
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        Quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Quit()
                        elif event.key == pygame.K_LALT and event.key == pygame.K_RETURN:
                            ROGUE_HUNTERWindow = pygame.display.toggle_fullscreen()
                        elif event.key == pygame.K_RETURN:
                            NextTurnSwitch = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if CurrentRedPlayerPosition[1] > 0:
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[1] -= 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentRedPlayerPosition[1] < (NumberOfLines-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[1] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentRedPlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NumberOfColumns-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BaseBlack, BaseBlue, BaseRed, BaseWhite)
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawMovements(ROGUE_HUNTERWindow, GridDimensions, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseBlack)
                if CurrentTurnMovements == MaxMovements or NextTurnSwitch == True:
                    CurrentPlayer = 'Blue'
                    NextTurnSwitch = False
                    CurrentTurnMovements = 0
                    break
                if RedMovements == 0 and BlueMovements == 0:
                    pass
                if CurrentBluePlayerPosition == CurrentRedPlayerPosition:
                    GameOver(ROGUE_HUNTERWindow, PlainTextFont, CurrentPlayer, BaseBlue, BaseRed)
                    pygame.event.clear()
                    pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        Quit()

# GENERAL VARIABLES
WindowDimensions = [0, 0]
GridDimensions = [0, 0]
PlayingGrid = {}
RedPlayerStart = [9, 4]
BluePlayerStart = [9, 15]
CurrentRedPlayerPosition = copy.deepcopy(RedPlayerStart)
CurrentBluePlayerPosition = copy.deepcopy(BluePlayerStart)
NumberOfColumns = 19
NumberOfLines = 20
MaxMovements = 10
FPS = 30

# COLOURS DEFINITION
BaseBlack = (0, 0, 0)
BaseWhite = (255, 255, 255)
BaseRed = (255, 0, 0)
BaseBlue = (0, 0, 255)
                

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
global FPSClock, ROGUE_HUNTERWindow, CurrentPlayer
PlayingGrid = GridConstructor(RedPlayerStart, BluePlayerStart, OuterSquareSize, StartingPointA, StartingPointB)

if __name__ == '__main__':
    main()