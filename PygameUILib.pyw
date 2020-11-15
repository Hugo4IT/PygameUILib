print("""
#===================================================#
#                                                   #
#   Title: PygameUI                                 #
#   Author: Hugo van de Kuilen from Hugo4IT         #
#   Website: Hugo4IT.com                            #
#   Special thanks: Glenn Mackintosh                #
#                                                   #
#===================================================#
""")

print("[PygameUILib] Loading Libraries...")

import os
import math
import numpy
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.gfxdraw
import pygame.freetype
from PygameAnimationLib import *

print("[PygameUILib] Loading PygameUILib...")

# Special thanks to Glenn Mackintosh on StackOverflow(https://stackoverflow.com/a/61961971)
# for creating draw_rounded_rect and draw_bordered_rounded_rect
def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)
def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)

loadedFonts = {}

global PUIL_CursorDragging
PUIL_CursorDragging = False

def Distance(x1, x2, y1, y2):
    return math.hypot(x2 - x1, y2 - y1)

def PreloadFont(fontname, *fontsizes):
    if ".ttf" in fontname:
        tFont = pygame.freetype.Font(fontname, fontsizes[0])
    else:
        tFont = pygame.font.SysFont(fontname, fontsizes[0])
    loadedFonts[fontname.replace(".ttf", "")+"."+str(fontsizes[0])] = tFont
    for x in fontsizes:
        if ".ttf" in fontname:
            tFont = pygame.freetype.Font(fontname, x)
        else:
            tFont = pygame.font.SysFont(fontname, x)
        loadedFonts[fontname.replace(".ttf", "")+"."+str(x)] = tFont

class Button():
    def __init__(self, *args):
        if len(args) == 5:
            self.x = args[0]            # X Position
            self.y = args[1]            # Y Position
            self.sx = args[2]           # X Size
            self.sy = args[3]           # Y Size
            self.color = args[4]        # Button Color
        elif len(args) == 1:
            self.x = 0
            self.y = 0
            self.sx = 100
            self.sy = 100
            self.color = pygame.Color("Red")
            tc = args[0].split("\n")
            for value in tc:
                if ":" in value:
                    k = value.split(":")[0]
                    v = value.split(":")[1].replace(" ", "").replace("\t", "")
                    if "//" in v :
                        v = v.split("//")[0]
                    if k == "position":
                        self.x = int(v.split(",")[0])
                        self.y = int(v.split(",")[1])
                    elif k == "size":
                        self.sx = int(v.split(",")[0])
                        self.sy = int(v.split(",")[1])
                    elif k == "color":
                        self.color = pygame.Color(str(v))
                        self.maincolor = pygame.Color(str(v))
                    elif k == "rounded":
                        self.rounded = v == "True"
                    elif k == "radius":
                        self.radius = int(v)
                    elif k == "bordered":
                        self.bordered = v == "True"
                    elif k == "bordersize":
                        self.bordersize = int(v)
                    elif k == "bordercolor":
                        self.bordercolor = pygame.Color(v)
                        self.mainbordercolor = pygame.Color(v)
                    elif k == "hovercolor":
                        self.hovercolor = pygame.Color(v)
                    elif k == "clickedcolor":
                        self.clickedcolor = pygame.Color(v)
                    elif k == "borderhovercolor":
                        self.borderhovercolor = pygame.Color(v)
                    elif k == "borderclickedcolor":
                        self.borderclickedcolor = pygame.Color(v)
                    elif k == "hidden":
                        self.hidden = v == "True"
                    elif k == "responsive":
                        self.responsive = v == "True"
                    elif k == "nonresponsivecolor":
                        self.nonresponsivecolor = pygame.Color(v)
            self.label = Label("Heloo, am snek", "Arial", 30, self.x, self.y, "#A911BD")

    def Draw(self, surface, fps = 60):
        if self.responsive:
            mpos = pygame.mouse.get_pos()
            if mpos[0] > self.x-self.sx/2 and mpos[0] < self.x+self.sx/2 and mpos[1] > self.y-self.sy/2 and mpos[1] < self.y+self.sy/2:
                if pygame.mouse.get_pressed(1)[0]:
                    self.color = self.clickedcolor
                    self.bordercolor = self.borderclickedcolor
                    if hasattr(self, 'func') and not self.hidden:
                        self.func()
                else:
                    self.color = self.hovercolor
                    self.bordercolor = self.borderhovercolor
            else:
                self.color = self.maincolor
                self.bordercolor = self.mainbordercolor
        else:
            color = self.nonresponsivecolor
        if not self.hidden:
            if not self.rounded:
                if not self.bordered:
                    pygame.draw.rect(surface, self.color, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy))
                else:
                    pygame.draw.rect(surface, self.bordercolor, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy))
                    pygame.draw.rect(surface, self.color, pygame.Rect(
                            self.x-self.sx/2+self.bordersize,
                            self.y-self.sy/2+self.bordersize,
                            self.sx-self.bordersize*2,
                            self.sy-self.bordersize*2
                    ))
            else:
                if not self.bordered:
                    draw_rounded_rect(surface, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy), self.color, self.radius)
                else:
                    draw_bordered_rounded_rect(surface, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy),
                            self.color, self.bordercolor, self.radius, self.bordersize)
        self.label.Draw(surface)

    def SetFunction(self, func):
        self.func = func

class Label():
    def __init__(self, *args):
        self.x = 0
        self.y = 0
        self.color = pygame.Color("Red")
        self.height = 1
        self.width = 1
        self.align = 2
        if len(args) == 1:
            self.x = 0
            self.y = 0
            self.sx = 100
            self.sy = 100
            self.color = pygame.Color("Red")
            tc = args[0].split("\n")
            for value in tc:
                if ":" in value:
                    k = value.split(":")[0]
                    v = value.split(":")[1].replace(" ", "").replace("\t", "")
                    if "//" in v :
                        v = v.split("//")[0]
                    if k == "position":
                        self.x = int(v.split(",")[0])
                        self.y = int(v.split(",")[1])
                    elif k == "fontcolor":
                        self.color = pygame.Color(v)
                    elif k == "hidden":
                        self.hidden = v == "True"
                    elif k == "align":
                        if v == "Left":
                            self.align = 0
                        if v == "Right":
                            self.align = 1
                        if v == "Middle" or v == "Center":
                            self.align = 2
        else:
            if args[1]+"."+str(args[2]) not in loadedFonts:
                PreloadFont(args[1], args[2])
            self.tfont = loadedFonts[args[1]+"."+str(args[2])]
            self.text = args[0]
            self.x = args[3]
            self.y = args[4]
            self.color = pygame.Color(args[5])

    def SetFont(self, font):
        if font not in loadedFonts:
            PreloadFont(font.split(".")[0], int(font.split(".")[1]))
        self.tfont = loadedFonts[font]

    def Draw(self, surface, fps = 60):
        if not self.hidden:
            text_surface = self.tfont.render(self.text, False, self.color)
            self.height = text_surface.get_height()
            self.width = text_surface.get_width()
            if self.align == 0:
                surface.blit(text_surface, (self.x, self.y-self.height/2))
            elif self.align == 1:
                surface.blit(text_surface, (self.x-self.width, self.y-self.height/2))
            elif self.align == 2:
                surface.blit(text_surface, (self.x-self.width/2, self.y-self.height/2))

class Slider():
    def __init__(self, config):
        self.x = 0
        self.y = 0
        self.width = 100
        self.linesize = 10
        self.knobsize = 5
        self.linecolor = pygame.Color("Red")
        self.knobcolor = pygame.Color("Red")
        self.value = 0
        self.max = 100
        self.responsive = True
        self.dragging = False
        tc = config.split("\n")
        for value in tc:
            if ":" in value:
                k = value.split(":")[0]
                v = value.split(":")[1].replace(" ", "").replace("\t", "")
                if "//" in v :
                    v = v.split("//")[0]
                if k == "position":
                    self.x = int(v.split(",")[0])
                    self.y = int(v.split(",")[1])
                elif k == "width":
                    self.width = int(v)
                elif k == "linesize":
                    self.linesize = int(v)
                elif k == "knobsize":
                    self.knobsize = int(v)
                elif k == "linecolor":
                    self.linecolor = pygame.Color(v)
                elif k == "knobcolor":
                    self.knobcolor = pygame.Color(v)
                elif k == "value":
                    self.value = int(v)
                elif k == "max":
                    self.max = int(v)
                elif k == "responsive":
                    self.responsive = v == "True"

    def Draw(self, surface, fps = 60):
        global PUIL_CursorDragging
        if Distance(int((self.x-self.width/2)+self.value*(self.width/self.max)), pygame.mouse.get_pos()[0], self.y, pygame.mouse.get_pos()[1]) <= self.knobsize:
            if self.responsive:
                if pygame.mouse.get_pressed(1)[0]:
                    if not PUIL_CursorDragging:
                        self.dragging = True
                        PUIL_CursorDragging = True
        if self.dragging:
            if pygame.mouse.get_pressed(1)[0] == False:
                self.dragging = False
                PUIL_CursorDragging = False
            tp = pygame.mouse.get_pos()
            if tp[0] < self.x-self.width/2:
                self.value = 0
            elif tp[0] > self.x+self.width/2:
                self.value = self.max
            else:
                tp2 = tp[0]
                tp2 -= self.x-self.width/2
                tp2 /= self.width/self.max
                self.value = tp2
        draw_rounded_rect(surface, pygame.Rect(self.x-self.width/2-self.knobsize+4, int(self.y-self.linesize/2), self.width+self.knobsize*2-8,
        int(self.linesize)), self.linecolor, int(math.floor(self.linesize/2)-2))
        pygame.draw.circle(surface, self.knobcolor, (int((self.x-self.width/2)+self.value*(self.width/self.max)), int(self.y)), self.knobsize)

print("[PygameUILib] Done!")
print()
