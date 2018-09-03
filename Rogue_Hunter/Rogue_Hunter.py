import sys
import math
import random
import pygame
from pygame.locals import *
from constants import *
import win32api
import copy
import time


# FUNCTIONS DEFINITIONS
#
# =====================
# BACKEND FUNCTIONS:

def GridConstructor(RedPosition, BluePosition, SquareSize, StartingPositionA, StartingPositionB):
    InputGrid = {}
    CurrentPositionA = copy.deepcopy(StartingPositionA)
    CurrentPositionB = copy.deepcopy(StartingPositionB)
    x = 0
    for Column in range(NUMBER_OF_COLUMNS):
        y = 0
        for Line in range(NUMBER_OF_LINES):
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
    BodyFontSize = int(DimensionValues[1] * 0.05)
    while (DimensionValues[0] / (BodyFontSize)) < 25:
        BodyFontSize -= 1
    FontDictionary["BodyFont"] = BodyFontSize, pygame.font.SysFont('visitortt1brk', BodyFontSize)
    print FontDictionary
    return FontDictionary

def WhiteGrid(InputGrid):
    for item, value in InputGrid.items():
        value[2] = 0

def Fullscreen (Window, WindowDimensions):
    flags = Window.get_flags()
    if flags == 0:
        Window = pygame.display.set_mode(WindowDimensions, pygame.FULLSCREEN)
    else:
        Window = pygame.display.set_mode(WindowDimensions)

def Quit():
    pygame.quit()
    sys.exit()

#     
#====================
#FRONT END FUNCTIONS:

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

def DrawMovements(Window, GridDimensions, FontList, BluePlayerMovements, RedPlayerMovements, Blue, Red, Black):
    BluePlayerScoreText = FontList["NumberFont"][1].render(str(BluePlayerMovements), False, Blue)
    RedPlayerScoreText = FontList["NumberFont"][1].render(str(RedPlayerMovements), False, Red)
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

def DrawScreen(InputGrid, Window, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BluePlayerMovements, RedPlayerMovements, Blue, Red, White, Black):
    pygame.draw.rect(Window, Black, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
    DrawingGrid(InputGrid, Window, OuterSquareSize, InnerSquareSize, Black, Blue, Red, White)
    DrawMovements(Window, GridDimensions, FontList, BluePlayerMovements, RedPlayerMovements, Blue, Red, Black)
    pygame.display.update()

def GameTitle(Window, WindowDimensions, FontDictionary, CurrentVersion):
    TitleWhite = [255, 255, 255, 0]
    Black = BASE_BLACK
    TitleLetters = ("R", "O", "G", "U", "E", " ", "H", "U", "N", "T", "E", "R")
    Title = FontDictionary["TitleFont"][1].render("ROGUE HUNTER", False, TitleWhite)
    TextWidth = Title.get_width()
    TextHeight = Title.get_height()
    TitleXPosition = (WindowDimensions[0] - TextWidth) / 2
    TitleYPosition = (WindowDimensions[1] / 2) - (TextHeight / 2)
    for letter in TitleLetters:
        if letter == " ":
           TitleXPosition += CurrentLetterWidth
        else:
            while TitleWhite[3] <= 100:
                CurrentLetter = FontDictionary["TitleFont"][1].render(letter, False, TitleWhite)
                Window.blit(CurrentLetter, (TitleXPosition, TitleYPosition))
                TitleWhite[3] += 1
                time.sleep(0.01)
                pygame.display.update()
            TitleWhite[3] = 0
            CurrentLetterWidth = CurrentLetter.get_width()
            TitleXPosition += CurrentLetterWidth
    Version = FontDictionary["BodyFont"][1].render(CurrentVersion, False, TitleWhite)
    VersionHeight = Version.get_height()
    VersionWidth = Version.get_width()
    VersionXPosition = (WindowDimensions[0] - VersionWidth) / 2
    VersionYPosition = TitleYPosition + TextHeight 
    while True:
        pygame.draw.rect(Window, Black, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
        Window.blit(Title, (TitleXPosition, TitleYPosition))
        Window.blit(Version, (VersionXPosition, VersionYPosition))
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

def GameOver(Window, FontList, Winner, Blue, Red, White):
    ScreenWidth = Window.get_width()
    ScreenHeight = Window.get_height()
    WinnerColour = 0
    if Winner == "Blue":
        WinnerColour = Blue
        FirstGameOverLine = FontList["BodyFont"][1].render('Game Over! Blue Player is the winner', False, WinnerColour)
        SecondGameOverLine = FontList["BodyFont"][1].render('Press a key to continue', False, WinnerColour)
        FirstLineWidth = FirstGameOverLine.get_width()
        FirstLineHeight = FirstGameOverLine.get_height()
        SecondLineWidth = SecondGameOverLine.get_width()
        FirstLinePosition = ((ScreenWidth - FirstLineWidth) / 2, (ScreenHeight / 2) - (FirstLineHeight - 2))
        SecondLinePosition = ((ScreenWidth - SecondLineWidth) / 2, (ScreenHeight / 2) + (FirstLineHeight + 2))
        Window.blit(FirstGameOverLine, FirstLinePosition)
        Window.blit(SecondGameOverLine, SecondLinePosition)
        pygame.display.update()
    elif Winner == "Red":
        WinnerColour = Red
        FirstGameOverLine = FontList["BodyFont"][1].render('Game Over! Red Player is the winner', False, WinnerColour)
        SecondGameOverLine = FontList["BodyFont"][1].render('Press a key to continue', False, WinnerColour)
        FirstLineWidth = FirstGameOverLine.get_width()
        FirstLineHeight = FirstGameOverLine.get_height()
        TextHeight = FirstGameOverLine.get_height()
        SecondLineWidth = SecondGameOverLine.get_width()
        FirstLinePosition = ((ScreenWidth - FirstLineWidth) / 2, (ScreenHeight / 2) - (FirstLineHeight - 2))
        SecondLinePosition = ((ScreenWidth - SecondLineWidth) / 2, (ScreenHeight / 2) + (FirstLineHeight + 2))
        Window.blit(FirstGameOverLine, FirstLinePosition)
        Window.blit(SecondGameOverLine, SecondLinePosition)
        pygame.display.update()
    else:
        WinnerColour = White
        FirstGameOverLine = FontList["BodyFont"][1].render('Both players run out of movements! Nobody won!', False, WinnerColour)
        SecondGameOverLine = FontList["BodyFont"][1].render('Press a key to continue', False, WinnerColour)
        FirstLineWidth = FirstGameOverLine.get_width()
        FirstLineHeight = FirstGameOverLine.get_height()
        TextHeight = FirstGameOverLine.get_height()
        SecondLineWidth = SecondGameOverLine.get_width()
        FirstLinePosition = ((ScreenWidth - FirstLineWidth) / 2, (ScreenHeight / 2) - (TextHeight - 2))
        SecondLinePosition = ((ScreenWidth - SecondLineWidth) / 2, (ScreenHeight / 2) + (TextHeight + 2))
        Window.blit(FirstGameOverLine, FirstLinePosition)
        Window.blit(SecondGameOverLine, SecondLinePosition)
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_f:
                Fullscreen(Window, WindowDimensions)
            else:
                Quit()

def GameInstructionsScreen(Window, FontDictionary, White, Black):
    WindowHeight = Window.get_height()
    WindowWidth = Window.get_width()
    HeaderX =  WindowHeight * 0.15
    BodyX = WindowHeight * 0.45
    BindingsX = WindowHeight * 0.25
    Position = copy.deepcopy(HeaderX)
    InstructionsHeader = FontDictionary["HeaderFont"][1].render('HOW TO PLAY:', False, White)
    FirstLine = FontDictionary["BodyFont"][1].render("1. There are two players: Red and Blue.", False, White)
    SecondLine = FontDictionary["BodyFont"][1].render("2. Each player has to catch the other player.", False, White)
    ThirdLine = FontDictionary["BodyFont"][1].render("3. Each player has 100 movements.", False, White)
    FourthLine = FontDictionary["BodyFont"][1].render("4. Each player can spend up to 10 movements per turn.", False, White)
    FifthLine = FontDictionary["BodyFont"][1].render("5. No player can pass the turn without moving.", False, White)
    SixthLine = FontDictionary["BodyFont"][1].render("6. The first player is chosen randomly.", False, White)
    SeventhLine = FontDictionary["BodyFont"][1].render("7. If both players run out of movements, nobody wins.", False, White)
    FirstBinding = FontDictionary["HeaderFont"][1].render('KEY BINDINGS', False, White)
    SecondBinding = FontDictionary["BodyFont"][1].render("W, S, A, D/ ARROW KEYS: Move", False, White)
    ThirddBinding = FontDictionary["BodyFont"][1].render("ENTER: End turn", False, White)
    FourthBinding = FontDictionary["BodyFont"][1].render("F: Fullscreen", False, White)
    FifthBinding = FontDictionary["BodyFont"][1].render("ESC: Quit", False, White)
    LastLine = FontDictionary["HeaderFont"][1].render('GOOD HUNT.', False, White)
    HeaderWidth = InstructionsHeader.get_width()
    HeaderPosition = (WindowWidth - HeaderWidth) / 2, (HeaderX - FontDictionary["HeaderFont"][0]) / 2
    InstructionsXPosition = {}
    InstructionsYPosition = WindowWidth * 0.1
    LineGap = ((BodyX - (FontDictionary["BodyFont"][0] * 7)) / 6)
    for line in range(7):
        InstructionsXPosition[line] = Position
        Position += FontDictionary["BodyFont"][0]
        Position += LineGap
    BindingsXPosition = {}
    BindingsYPosition = {}
    FirstBindingWidth = FirstBinding.get_width()
    SecondBindingWidth = SecondBinding.get_width()
    ThirdBindingWidth = ThirddBinding.get_width()
    FourthBindingWidth = FourthBinding.get_width()
    FifthBindingWidth = FifthBinding.get_width()
    BindingsFirstYGap = (WindowWidth - (SecondBindingWidth + ThirdBindingWidth)) / 3
    BindingsSecondYGap = (WindowWidth - (FourthBindingWidth + FifthBindingWidth)) / 3
    for line in range(3):
        BindingsXPosition[line] = Position
        if line == 0:
            Position += FontDictionary["HeaderFont"][0]
        else:
            Position += (FontDictionary["BodyFont"][0] + WindowHeight*0.02)
    for item in range(5):
        if item == 0:
            BindingsYPosition[item] = (WindowWidth - FirstBindingWidth) / 2
        elif item == 1:
            BindingsYPosition[item] = BindingsFirstYGap
        elif item == 2:
            BindingsYPosition[item] = (BindingsFirstYGap * 2) + SecondBindingWidth
        elif item == 3:
            BindingsYPosition[item] = BindingsSecondYGap
        elif item == 4:
            BindingsYPosition[item] = (BindingsSecondYGap * 2) + FourthBindingWidth
    LastLineWidth = LastLine.get_width()
    LastLinePosition = (WindowWidth - LastLineWidth) / 2, WindowHeight * 0.85
    while True:
        pygame.draw.rect(Window, Black, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
        Window.blit(InstructionsHeader, HeaderPosition)
        Window.blit(FirstLine, (InstructionsYPosition, InstructionsXPosition[0]))
        Window.blit(SecondLine, (InstructionsYPosition, InstructionsXPosition[1]))
        Window.blit(ThirdLine, (InstructionsYPosition, InstructionsXPosition[2]))
        Window.blit(FourthLine, (InstructionsYPosition, InstructionsXPosition[3]))
        Window.blit(FifthLine, (InstructionsYPosition, InstructionsXPosition[4]))
        Window.blit(SixthLine, (InstructionsYPosition, InstructionsXPosition[5]))
        Window.blit(SeventhLine, (InstructionsYPosition, InstructionsXPosition[6]))
        Window.blit(FirstBinding, (BindingsYPosition[0], BindingsXPosition[0]))
        Window.blit(SecondBinding, (BindingsYPosition[1], BindingsXPosition[1]))
        Window.blit(ThirddBinding, (BindingsYPosition[2], BindingsXPosition[1]))
        Window.blit(FourthBinding, (BindingsYPosition[3], BindingsXPosition[2]))
        Window.blit(FifthBinding,(BindingsYPosition[4], BindingsXPosition[2]))
        Window.blit(LastLine, LastLinePosition)
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

#MAIN LOOP

def main():
    pygame.init()
    pygame.font.init()
    FontList = TextfontCalculator(WindowDimensions)
    CurrentPlayer = FirstPlayerSelector()
    RedMovements = copy.deepcopy(STARTING_MOVEMENTS)
    BlueMovements =  copy.deepcopy(STARTING_MOVEMENTS)
    CurrentTurnMovements = 0
    NextTurnSwitch = False
    pygame.display.set_caption('Rogue Hunter')
    ROGUE_HUNTERWindow = pygame.display.set_mode(WindowDimensions)
    GameTitle(ROGUE_HUNTERWindow, WindowDimensions, FontList, CURRENT_VERSION)
    GameInstructionsScreen(ROGUE_HUNTERWindow, FontList, BASE_WHITE, BASE_BLACK)
    DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
    while True:
        if CurrentPlayer == 'Blue':
            TurnChange(ROGUE_HUNTERWindow, FontList, CurrentPlayer, BASE_BLUE, BASE_RED)
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        Quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Quit()
                        elif event.key == pygame.K_f:
                            Fullscreen(ROGUE_HUNTERWindow, WindowDimensions)
                            DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
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
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentBluePlayerPosition[1] < (NUMBER_OF_LINES - 1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[1] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentBluePlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NUMBER_OF_COLUMNS-1):
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 0
                                CurrentBluePlayerPosition[0] += 1
                                PlayingGrid[str(CurrentBluePlayerPosition)][2] = 1
                                CurrentTurnMovements += 1
                                BlueMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                if CurrentTurnMovements == MAX_MOVEMENTS or NextTurnSwitch == True:
                    CurrentPlayer = 'Red'
                    NextTurnSwitch = False
                    CurrentTurnMovements = 0
                    break
                if CurrentBluePlayerPosition == CurrentRedPlayerPosition:
                    WhiteGrid(PlayingGrid)
                    pygame.draw.rect(ROGUE_HUNTERWindow, BASE_BLACK, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BASE_BLACK, BASE_BLUE, BASE_RED, BASE_WHITE)
                    Winner = "Blue"
                    GameOver(ROGUE_HUNTERWindow, FontList, Winner, BASE_BLUE, BASE_RED, BASE_WHITE)
                if BlueMovements == 0 and RedMovements == 0:
                    pygame.draw.rect(ROGUE_HUNTERWindow, BASE_BLACK, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
                    Winner = "None"
                    GameOver(ROGUE_HUNTERWindow, FontList, Winner, BASE_BLUE, BASE_RED, BASE_WHITE)
        elif CurrentPlayer == 'Red':
            TurnChange(ROGUE_HUNTERWindow, FontList, CurrentPlayer, BASE_BLUE, BASE_RED)
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        Quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Quit()
                        elif event.key == pygame.K_f:
                            Fullscreen(ROGUE_HUNTERWindow, WindowDimensions)
                            DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
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
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if CurrentRedPlayerPosition[1] < (NUMBER_OF_LINES-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[1] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if CurrentRedPlayerPosition[0] > 0:
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] -= 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if CurrentBluePlayerPosition[0] < (NUMBER_OF_COLUMNS-1):
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 0
                                CurrentRedPlayerPosition[0] += 1
                                PlayingGrid[str(CurrentRedPlayerPosition)][2] = 2
                                CurrentTurnMovements += 1
                                RedMovements -= 1
                                DrawScreen(PlayingGrid, ROGUE_HUNTERWindow, WindowDimensions, GridDimensions, OuterSquareSize, InnerSquareSize, FontList, BlueMovements, RedMovements, BASE_BLUE, BASE_RED, BASE_WHITE, BASE_BLACK)
                if CurrentTurnMovements == MAX_MOVEMENTS or NextTurnSwitch == True:
                    CurrentPlayer = 'Blue'
                    NextTurnSwitch = False
                    CurrentTurnMovements = 0
                    break
                if RedMovements == 0 and BlueMovements == 0:
                    pass
                if CurrentBluePlayerPosition == CurrentRedPlayerPosition:
                    WhiteGrid(PlayingGrid)
                    pygame.draw.rect(ROGUE_HUNTERWindow, BASE_BLACK, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
                    DrawingGrid(PlayingGrid, ROGUE_HUNTERWindow, OuterSquareSize, InnerSquareSize, BASE_BLACK, BASE_BLUE, BASE_RED, BASE_WHITE)
                    Winner = "Red"
                    GameOver(ROGUE_HUNTERWindow, FontList, Winner, BASE_BLUE, BASE_RED, BASE_WHITE)
                if BlueMovements == 0 and RedMovements == 0:
                    pygame.draw.rect(ROGUE_HUNTERWindow, BASE_BLACK, (0, 0, WindowDimensions[0], WindowDimensions[1]), 0)
                    Winner = "None"
                    GameOver(ROGUE_HUNTERWindow, FontList, Winner, BASE_BLUE, BASE_RED, BASE_WHITE)

# GENERAL VARIABLES
WindowDimensions = [0, 0]
GridDimensions = [0, 0]
PlayingGrid = {}
CurrentRedPlayerPosition = copy.deepcopy(RED_PLAYER_START)
CurrentBluePlayerPosition = copy.deepcopy(BLUE_PLAYER_START)

                
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
PlayingGrid = GridConstructor(RED_PLAYER_START, BLUE_PLAYER_START, OuterSquareSize, StartingPointA, StartingPointB)

if __name__ == '__main__':
    main()