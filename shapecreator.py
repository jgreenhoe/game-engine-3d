#move windows on screen
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '957,0'

#initialize tkinter
import tkinter as tk
root = tk.Tk()
root.geometry('957x1015')
root.update_idletasks()

#initialize pygame
import pygame
pygame.init()
screen = [958,1015]
surface = pygame.display.set_mode(screen)
pygame.display.set_caption("Shape Creator")

while True:
    root.update_idletasks()
    pygame.display.update()