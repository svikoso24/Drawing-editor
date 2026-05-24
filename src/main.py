"""
Simple raster drawing editor made in pygame.

Features:
- drawing
- zoom
- pan
- saving images
- color selection
"""

import pygame
# import tkinter as tk
# import random

def main() -> None:
    """spusti drawing editor"""
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont('Consolas', 30)

    zoom = 1.0
    offset_x = 0
    offset_y = 0

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
    cyan = (0, 255, 225)

    editor_rect = pygame.Rect(0, 91, 1280, height-91)
    editor = pygame.Surface((1280, height-91))
    bg_fill_editor = white
    editor.fill((bg_fill_editor))
    undo_stack = []
    redo_stack = []

    # text_color = font.render("Color: ", True, (100,100,100))

    class Button:
        def __init__(self, x, y, w, h, text, callback, color=(212,205,205)):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = text
            self.callback = callback
            self.was_pressed = False
            self.color = color

        def draw(self, surface) -> None:
            """vykresli tlacitko"""
            pygame.draw.rect(surface, self.color, self.rect)

            surf_text = font.render(self.text, True, (0,0,0)) 
            rect_text = surf_text.get_rect(center=self.rect.center)

            surface.blit(surf_text, rect_text)

        def update(self, mouse_pos) -> bool:
            """obnovi pozivci mysi"""
            return self.rect.collidepoint(mouse_pos)
        

    mouse_color = black
    def set_color(color) -> None:
        """nastavi barvu"""
        nonlocal mouse_color 
        mouse_color = color
        # self.setOpacity(0.7)

    def clear() -> None:
        """vymaze cele platno"""
        editor.fill((white))

    typing_name = False
    filename = ""
    def save() -> None:
        """zacne psani nazvu souboru"""
        nonlocal typing_name, filename
        typing_name = True
        filename = ""

    brush_size = 8
    def size() -> None:
        ...
    def plus() -> None:
        """zvetsi tloustku stetce"""
        nonlocal brush_size, size_btn
        if brush_size >= 30:
            brush_size = 30
            return
        brush_size += 2
        size_btn.text = str(brush_size)
    def minus() -> None:
        """zmensi tloustku stetce"""
        nonlocal brush_size, size_btn
        if brush_size <= 2:
            brush_size = 2
            return
        brush_size -= 2
        size_btn.text = str(brush_size)

    def eraser() -> None:
        """guma"""
        nonlocal mouse_color 
        mouse_color = bg_fill_editor

    def undo() -> None:
        """vratit zpatky"""
        nonlocal editor
        if undo_stack:
            redo_stack.append(editor.copy())
            editor = undo_stack.pop() #posledni stary stav
    def redo() -> None:
        """jit dopredu"""
        nonlocal editor
        if redo_stack:
            undo_stack.append(editor.copy())
            editor = redo_stack.pop() #posledni stary stav


    save_btn = Button(30, 25, 100, 40, "Save", save)
    clear_btn = Button(140, 25, 100, 40, "Clear", clear)
    black_btn = Button(260, 20, 40, 25, "", lambda: set_color(black), black)
    white_btn = Button(260, 50, 40, 25, "", lambda: set_color(white), white)
    red_btn = Button(310, 20, 40, 25, "", lambda: set_color(red), red)
    orange_btn = Button(310, 50, 40, 25, "", lambda: set_color(orange), orange)
    yellow_btn = Button(360, 20, 40, 25, "", lambda: set_color(yellow), yellow)
    green_btn = Button(360, 50, 40, 25, "", lambda: set_color(green), green)
    blue_btn = Button(410, 20, 40, 25, "", lambda: set_color(blue), blue)
    purple_btn = Button(410, 50, 40, 25, "", lambda: set_color(purple), purple)
    pink_btn = Button(460, 20, 40, 25, "", lambda: set_color(pink), pink)
    cyan_btn = Button(460, 50, 40, 25, "", lambda: set_color(cyan), cyan)
    size_btn = Button(510, 20, 35, 55, str(brush_size), size)
    plus_btn = Button(550, 20, 30, 25, "+", plus)
    minus_btn = Button(550, 50, 30, 25, "-", minus)
    eraser_btn = Button(590, 25, 100, 40, "Eraser", eraser)
    undo_btn = Button(700, 20, 50, 25, "<-", undo)
    redo_btn = Button(700, 50, 50, 25, "->", redo)

    buttons = [save_btn, clear_btn, size_btn, plus_btn, minus_btn, eraser_btn, undo_btn, redo_btn]
    colors = [black_btn, white_btn, red_btn, orange_btn, yellow_btn, green_btn, blue_btn, purple_btn, pink_btn, cyan_btn]
    drawing = False

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
                        undo_stack.append(editor.copy()) #kopie platna se ulozi
                        redo_stack.clear() #vymazou se kopie
                        drawing = True
                        last_pos = event.pos # kreslím od posledního bodu k aktuálnímu
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    last_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    mx, my = event.pos

                    x = (mx - offset_x) / zoom
                    y = (my - offset_y-91) / zoom

                    last_x = (last_pos[0] - offset_x) / zoom
                    last_y = (last_pos[1] - offset_y-91) / zoom
                    
                    pygame.draw.line(editor, mouse_color, (last_x, last_y), (x, y), brush_size)
                    last_pos = event.pos
                    # pygame.draw.line(editor, mouse_color, last_pos, event.pos, brush_size)
                    # z bodu (last_x, last_y) -- do bodu (x, y)
                    # x = vodorovný, y = svislý -- (100, 200) == 100 pixelů doprava, 200 pixelů dolů
                elif pygame.mouse.get_pressed()[2]:
                    offset_x += event.rel[0]
                    offset_y += event.rel[1]
                    # = o kolik se myš pohnula od posledního momentu (dx, dy)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom += 0.1
                else:
                    zoom -= 0.1
                zoom = max(0.2, min(zoom, 3)) #limit (0.2x až 3x)
            elif event.type == pygame.KEYDOWN:
                if typing_name: 
                    if event.key == pygame.K_RETURN: #enter
                        if filename != "":
                            pygame.image.save(editor, filename + ".png")
                            print("saved as "+filename+".png")
                        typing_name = False
                    elif event.key == pygame.K_BACKSPACE: 
                        filename = filename[:-1] #smaze posledni znak
                    elif event.key == pygame.K_ESCAPE:
                        typing_name = False
                    else:
                        filename += event.unicode #znak co uzivatel naspal

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

        
        scaled_width = int(1280*zoom)
        scaled_height = int((height-91)*zoom)
        scaled_editor = pygame.transform.scale(editor, (scaled_width, scaled_height))
        screen.blit(scaled_editor, (offset_x, offset_y+91))
        
        if typing_name: #input na psani nazvu souboru
            pygame.draw.rect(screen, white, (800, 20, 250, 40))
            pygame.draw.rect(screen, black, (800, 20, 250, 40), 2) #border

            text = font.render(filename, True, black)
            screen.blit(text, (810, 25))

        pygame.display.update()
        clock.tick(2000)

    pygame.quit()
    
if __name__ == "__main__":
    main()