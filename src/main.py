import pygame
# import tkinter as tk
# import random


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Consolas', 30)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#colors
white = (255,255,255)
black = (0,0,0)
red = (209,19,19)
orange = (237,134,43)
yellow = (237,211,43)
green = (38,184,35)
blue = (41,118,227)
purple = (196,93,240)
pink = (240,93,193)

editor_rect = pygame.Rect(0, 91, 1280, height-91)
editor = pygame.Surface((1280, height-91))
editor.fill((255, 255, 255))

# text_color = font.render("Color: ", True, (100,100,100))

class Button:
    def __init__(self, x, y, w, h, text, callback, color=(212,205,205)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.was_pressed = False
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        surf_text = font.render(self.text, True, (0,0,0)) 
        rect_text = surf_text.get_rect(center=self.rect.center)

        surface.blit(surf_text, rect_text)

    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0] and not self.was_pressed:
                if self.callback:
                    self.callback()
                self.was_pressed = True
            else:
                self.was_pressed = False
        else:
            self.was_pressed = False
    

mouse_color = black
def set_color(color):
    global mouse_color 
    mouse_color = color
    # self.setOpacity(0.7)
def clear():
    editor.fill((white))
def save():
    ...
save_btn = Button(30, 30, 100, 40, "Save", save)
clear_btn = Button(140, 30, 100, 40, "Clear", clear)
black_btn = Button(260, 30, 40, 40, "", lambda: set_color(black), black)
red_btn = Button(310, 30, 40, 40, "", lambda: set_color(red), red)
orange_btn = Button(360, 30, 40, 40, "", lambda: set_color(orange), orange)
yellow_btn = Button(410, 30, 40, 40, "", lambda: set_color(yellow), yellow)
green_btn = Button(460, 30, 40, 40, "", lambda: set_color(green), green)
blue_btn = Button(510, 30, 40, 40, "", lambda: set_color(blue), blue)
purple_btn = Button(560, 30, 40, 40, "", lambda: set_color(purple), purple)
pink_btn = Button(610, 30, 40, 40, "", lambda: set_color(pink), pink)

buttons = [save_btn, clear_btn]
colors = [black_btn, red_btn, orange_btn, yellow_btn, green_btn, blue_btn, purple_btn, pink_btn]
drawing = False
brush_size = 8

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.callback()
                        clicked_button = True
                        break
                else:
                    for color in colors:
                        if color.rect.collidepoint(event.pos):
                            color.callback()
                            clicked_color = True
                            break
                    else:
                        if editor_rect.collidepoint(event.pos):
                            drawing = True
                            last_pos = event.pos # kreslím od posledního bodu k aktuálnímu
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                x, y = event.pos
                last_x, last_y = last_pos
                y -= 91
                last_y -= 91
                pygame.draw.line(editor, mouse_color, (last_x, last_y), (x, y), brush_size)
                last_pos = event.pos
                # pygame.draw.line(editor, mouse_color, last_pos, event.pos, brush_size)
                # z bodu (last_x, last_y) -- do bodu (x, y)
                # x = vodorovný, y = svislý -- (100, 200) == 100 pixelů doprava, 200 pixelů dolů
                

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    # [0] = left
    # [1] = center
    # [2] = right

    screen.fill((100,100,100))
    save_btn.update(mouse_pos, mouse_click)
    for button in buttons:
        button.draw(screen)
    for color in colors:
        color.draw(screen)

    screen.blit(editor, (0, 91))
    
    pygame.display.update()
    clock.tick(20)

pygame.quit()
