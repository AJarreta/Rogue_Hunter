import sys
import math
import pygame
import win32api

# COLOURS DEFINITION
BaseBlack = (0, 0, 0)
BaseWhite = (255, 255, 255)
BaseRed = (255, 0, 0)
BaseBlue = (0, 0, 255)

ScreenWidth = win32api.GetSystemMetrics(0)
ScreenHeight = win32api.GetSystemMetrics(1)
WindowDimensions = [win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]

print ScreenWidth, ScreenHeight

GridHeight = int(ScreenHeight*0.8)
while (GridHeight % 20) != 0:
    GridHeight -= 1
GridWidth = int(GridHeight*0.95)
BaseSquareSize = GridHeight/20

print GridWidth, GridHeight

pygame.init()
while True:
    Window = pygame.display.set_mode(WindowDimensions)
    pygame.draw.rect(Window, BaseWhite, (BaseSquareSize, BaseSquareSize, BaseSquareSize, BaseSquareSize), 0)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONCLICK and event.button(1):
            pygame.quit()
            sys.exit()
