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

def FirstPlayerSelector():
    RandomNumber = random.randint(1, 2)
    if RandomNumber == 1:
        FirstPlayer = "Red"
    else:
        FirstPlayer = "Blue"
    return FirstPlayer

def TextfontCalculator(DimensionValues):
    FontDictionary = {}
    TitleFontSize = int(DimensionValues[1] * 0.25)
    while (DimensionValues[0] / TitleFontSize) < 8:
        print TitleFontSize
        TitleFontSize -= 1
    FontDictionary["TitleFont"] = TitleFontSize, pygame.font.SysFont('visitortt1brk', TitleFontSize)
    NumberFontSize = int(DimensionValues[1] * 0.20)
    while (DimensionValues[0] / (NumberFontSize)) < 8:
        NumberFontSize -= 1
    FontDictionary["NumberFont"] = NumberFontSize, pygame.font.SysFont('visitortt1brk', NumberFontSize)
    HeaderFontSize = int(DimensionValues[1] * 0.10)
    while (DimensionValues[0] / (HeaderFontSize)) < 15:
        HeaderFontSize -= 1
    FontDictionary["HeaderFont"] = HeaderFontSize, pygame.font.SysFont('visitortt1brk', HeaderFontSize)
    BodyFontSize = int((DimensionValues[1] * 0.05) * 0.75)
    while (DimensionValues[0] / (BodyFontSize)) < 25:
        BodyFontSize -= 1
    FontDictionary["BodyFont"] = BodyFontSize, pygame.font.SysFont('visitortt1brk', BodyFontSize)
    print FontDictionary
    return FontDictionary

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
    Window.blit(BluePlayerScoreText, (BlueScoreXPosition, ScoreYPosition))
    Window.blit(RedPlayerScoreText, (RedScoreXPosition, ScoreYPosition))

def DrawScreen(InputGrid, Window, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, TextFont, BluePlayerMovements, RedPlayerMovements, Blue, Red, White, Black):
    pygame.draw.rect(Window, Black, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
    DrawingGrid(InputGrid, Window, OuterSquareSize, InnerSquareSize, Black, Blue, Red, White)
    DrawMovements(Window, GridDimensions, TextFont, BluePlayerMovements, RedPlayerMovements, Blue, Red, Black)
    pygame.display.update()

def GameTitle(Window, WindowDimensions, TextFont, White, Black):
    Title = TextFont.render("ROGUE HUNTER", False, White)
    TextWidth = Title.get_width()
    TextHeight = Title.get_height()
    TitleXPosition = (WindowDimensions[0] - TextWidth) / 2
    TitleYPosition = (WindowDimensions[1] / 2) - (TextHeight / 2)
    while True:
        pygame.draw.rect(Window, Black, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
        Window.blit(Title, (TitleXPosition, TitleYPosition))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    Quit()
                elif event.key == K_f:
                    Fullscreen(Window, WindowDimensions)
                else:
                    return

def TurnChange(Window, FontDictionary, CurrentPlayer, Blue, Red):
    ScreenWidth = Window.get_width()
    ScreenHeight = Window.get_height()
    if CurrentPlayer == 'Blue':
        CurrentPlayerColour = Blue
    else:
        CurrentPlayerColour = Red
    TurnChangeText = FontDictionary["BodyFont"][1].render(CurrentPlayer + " Player Turn", False, CurrentPlayerColour)
    TextWidth = TurnChangeText.get_width()
    TextHeight = TurnChangeText.get_height()
    TextPosition = ((ScreenWidth - TextWidth) / 2, (ScreenHeight / 2) - (TextHeight / 2))
    Window.blit(TurnChangeText, TextPosition)
    pygame.display.update()

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
    SecondGameOverLine = TextFont.render('Press a key to continue', False, CurrentPlayerColour)
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

def GameInstructionsScreen(Window, FontDictionary, BaseWhite, BaseBlack):
    WindowHeight = Window.get_height()
    WindowWidth = Window.get_width()
    HeaderX =  WindowHeight * 0.15
    BodyX = WindowHeight * 0.45
    BindingsX = WindowHeight * 0.25
    InstructionsHeader = FontDictionary["HeaderFont"][1].render('HOW TO PLAY:', False, BaseWhite)
    HeaderWidth = InstructionsHeader.get_width()
    HeaderHeight = InstructionsHeader.get_height()
    HeaderPosition = ((WindowWidth - HeaderWidth) / 2, (HeaderX - HeaderHeight) / 2)
    InstructionsXPosition = {}
    InstuctionsYPosition = WindowWidth * 0.1
    Position = copy.deepcopy(HeaderX)
    LineGap = ((BodyX - (FontDictionary["BodyFont"][0] * 7)) / 6)
    print LineGap
    for line in range(7):
        InstructionsXPosition[line] = Position
        Position += FontDictionary["BodyFont"][0]
        Position += LineGap
        print Position
    FirstLine = FontDictionary["BodyFont"][1].render("1. There are two players: Red and Blue.", False, BaseWhite)
    SecondLine = FontDictionary["BodyFont"][1].render("2. Each player has to catch the other player.", False, BaseWhite)
    ThirdLine = FontDictionary["BodyFont"][1].render("3. Each player has 100 movements.", False, BaseWhite)
    FourthLine = FontDictionary["BodyFont"][1].render("4. Each player can spend up to 10 movements per turn.", False, BaseWhite)
    FifthLine = FontDictionary["BodyFont"][1].render("5. No player can pass the turn without moving.", False, BaseWhite)
    SixthLine = FontDictionary["BodyFont"][1].render("6. The first player is chosen randomly.", False, BaseWhite)
    SeventhLine = FontDictionary["BodyFont"][1].render("7. If both players run out of movements, nobody wins.", False, BaseWhite)

        
        
    
    while True:
        pygame.draw.rect(Window, BaseBlack, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
        Window.blit(InstructionsHeader, HeaderPosition)
        Window.blit(FirstLine, (InstuctionsYPosition, InstructionsXPosition[0]))
        Window.blit(SecondLine, (InstuctionsYPosition, InstructionsXPosition[1]))
        Window.blit(ThirdLine, (InstuctionsYPosition, InstructionsXPosition[2]))
        Window.blit(FourthLine, (InstuctionsYPosition, InstructionsXPosition[3]))
        Window.blit(FifthLine, (InstuctionsYPosition, InstructionsXPosition[4]))
        Window.blit(SixthLine, (InstuctionsYPosition, InstructionsXPosition[5]))
        Window.blit(SeventhLine, (InstuctionsYPosition, InstructionsXPosition[6]))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    Quit()
                elif event.key == K_f:
                    Fullscreen(Window, WindowDimensions)
                else:
                    return

def Fullscreen (Window, WindowDimensions):
    flags = Window.get_flags()
    print flags
    if flags == 0:
        Window = pygame.display.set_mode(WindowDimensions, pygame.FULLSCREEN)
    else:
        Window = pygame.display.set_mode(WindowDimensions)

def Quit():
    pygame.quit()
    sys.exit()

#MAIN LOOP
def main():
    pygame.init()
    pygame.font.init()
    FontList = TextfontCalculator(WindowDimensions)
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
    GameTitle(ROGUE_HUNTERWindow, WindowDimensions, FontList["TitleFont"][1], BaseWhite, BaseBlack)
    GameInstructionsScreen(ROGUE_HUNTERWindow, FontList, BaseWhite, BaseBlack)
    DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
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
                            Fullscreen(ROGUE_HUNTERWindow, WindowDimensions)
                            DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_RETURN:
                            if CurrentTurnMovements == 0:
                                pass
                            else:
                                NextTurnSwitch = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if CurrentBluePlayerPosition[1] > 0:
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[1] -= 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentBluePlayerPosition[1] < (NumberOfLines - 1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[1] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentBluePlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NumberOfColumns-1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
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
                        elif event.key == pygame.K_f:
                            Fullscreen(ROGUE_HUNTERWindow, WindowDimensions)
                            DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_RETURN:
                            if CurrentTurnMovements == 0:
                                pass
                            else:
                                NextTurnSwitch = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if CurrentRedPlayerPosition[1] > 0:
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[1] -= 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentRedPlayerPosition[1] < (NumberOfLines-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[1] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentRedPlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NumberOfColumns-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, NumberFont, BlueMovements, RedMovements, BaseBlue, BaseRed, BaseWhite, BaseBlack)
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