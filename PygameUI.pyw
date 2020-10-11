
#===================================================#
#                                                   #
#   Title: PygameUI                                 #
#   Author: Hugo van de Kuilen from Hugo4IT         #
#   Website: Hugo4IT.com                            #
#   Special thanks: Glenn Mackintosh                #
#                                                   #
#===================================================#

import pygame
import pygame.gfxdraw
import pygame.freetype

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
            self.label = Label("Heloo, am snek", "Arial", 30, 500, 500, "Red")

    def Draw(self, surface):
        if self.responsive:
            mpos = pygame.mouse.get_pos()
            if mpos[0] > self.x and mpos[0] < self.x+self.sx and mpos[1] > self.y and mpos[1] < self.y+self.sy:
                if pygame.mouse.get_pressed(1)[0]:
                    self.color = self.clickedcolor
                    self.bordercolor = self.borderclickedcolor
                    if hasattr(self, 'func'):
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
                    pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.sx, self.sy))
                else:
                    pygame.draw.rect(surface, self.bordercolor, pygame.Rect(self.x, self.y, self.sx, self.sy))
                    pygame.draw.rect(surface, self.color, pygame.Rect(
                            self.x+self.bordersize,
                            self.y+self.bordersize,
                            self.sx-self.bordersize*2,
                            self.sy-self.bordersize*2
                    ))
            else:
                if not self.bordered:
                    draw_rounded_rect(surface, pygame.Rect(self.x, self.y, self.sx, self.sy), self.color, self.radius)
                else:
                    draw_bordered_rounded_rect(surface, pygame.Rect(self.x, self.y, self.sx, self.sy),
                            self.color, self.bordercolor, self.radius, self.bordersize)
        self.label.Draw(surface)

    def SetFunction(self, func):
        self.func = func

class Label():
    def __init__(self, *args):
        if args[1]+"."+str(args[2]) not in loadedFonts:
            PreloadFont(args[1], args[2])
        self.text = args[0]
        self.tfont = loadedFonts[args[1]+"."+str(args[2])]
        self.x = args[3]
        self.y = args[4]
        self.color = pygame.Color(args[5])
        self.height = 1
        self.width = 1

    def Draw(self, surface):
        text_surface = self.tfont.render(self.text, False, self.color)
        self.height = text_surface.get_height()
        self.width = text_surface.get_width()
        surface.blit(text_surface, (self.x, self.y))
