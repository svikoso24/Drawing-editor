import pygame
# import tkinter as tk
# import random

def main():
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

        def update(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)
        

    mouse_color = black
    def set_color(color):
        nonlocal mouse_color 
        mouse_color = color
        # self.setOpacity(0.7)
    def clear():
        editor.fill((white))
    def save():
        pygame.image.save(editor, "drawing.png")
        print("saved as drawing.png")
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
                            break
                    for color in colors:
                        if color.rect.collidepoint(event.pos):
                            color.callback()
                            break
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
        # [0] = left
        # [1] = center
        # [2] = right

        screen.fill((100,100,100))
        for button in buttons:
            button.draw(screen)
            button.update(mouse_pos)
        for color in colors:
            color.draw(screen)
            color.update(mouse_pos)

        screen.blit(editor, (0, 91))
        
        pygame.display.update()
        clock.tick(20)

    pygame.quit()
    
if __name__ == "__main__":
    main()