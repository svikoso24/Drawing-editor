import pygame
# import tkinter
# import random


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Consolas', 30)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#colors
white = (250, 250, 250)
black = (0,0,0)
red = (209,19,19)
orange = (237,134,43)
yellow = (237,211,43)
green = (38,184,35)
blue = (41,118,227)
purple = (196,93,240)
pink = (240,93,193)

running = True

editor = pygame.Rect((0, 91, width, height-91))

class Button:
    def __init__(self, x, y, w, h, text, callback, color=(212,205,205)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

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
    

def on_button_click():
    ...
    # mouse_color = self.color
    # self.setOpacity(0.7)
save_btn = Button(30, 30, 100, 40, "Save", on_button_click)
clear_btn = Button(140, 30, 100, 40, "Clear", on_button_click)
black_btn = Button(260, 30, 40, 40, "", on_button_click, black)
red_btn = Button(310, 30, 40, 40, "", on_button_click, red)
orange_btn = Button(360, 30, 40, 40, "", on_button_click, orange)
yellow_btn = Button(410, 30, 40, 40, "", on_button_click, yellow)
green_btn = Button(460, 30, 40, 40, "", on_button_click, green)
blue_btn = Button(510, 30, 40, 40, "", on_button_click, blue)
purple_btn = Button(560, 30, 40, 40, "", on_button_click, purple)
pink_btn = Button(610, 30, 40, 40, "", on_button_click, pink)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    save_btn.update(mouse_pos, mouse_click)
    
    screen.fill((230, 230, 230))
    save_btn.draw(screen)
    clear_btn.draw(screen)
    black_btn.draw(screen)
    red_btn.draw(screen)
    orange_btn.draw(screen)
    yellow_btn.draw(screen)
    green_btn.draw(screen)
    blue_btn.draw(screen)
    purple_btn.draw(screen)
    pink_btn.draw(screen)

    pygame.draw.line(screen, black, (width, 90), (0, 90))
    pygame.draw.rect(screen, white, editor)
    
    pygame.display.update()
    clock.tick(20)

pygame.quit()
