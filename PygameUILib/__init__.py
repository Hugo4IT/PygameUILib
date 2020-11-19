print("""
#===================================================#
#                                                   #
#   Title: PygameUILib                              #
#   Author: Hugo van de Kuilen from Hugo4IT         #
#   Website: Hugo4IT.com                            #
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

# Special thanks to andreas dr and Eli on StackOverflow(https://stackoverflow.com/a/62480486)
# for creating draw_circle
def draw_circle(surface, x, y, radius, color):
    pygame.gfxdraw.aacircle(surface, x, y, radius, color)
    pygame.gfxdraw.filled_circle(surface, x, y, radius, color)

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

class IFType(Enum):
    Text = 0
    Multiline = 1
    Number = 2

class Button():
    def __init__(self, *args):

        #Initialize Animations
        self.ColorAnimationValue = AnimatableValue(pygame.Color("Red"))
        self.ColorAnimation = Animation(self.ColorAnimationValue, From=pygame.Color("Red"), To=pygame.Color("Blue"),
                                        Duration=0.5, Ease=EaseTypes.EaseOut)
        self.ColorAnimation.Play()
        self.BorderColorAnimationValue = AnimatableValue(pygame.Color("Red"))
        self.BorderColorAnimation = Animation(self.BorderColorAnimationValue, From=pygame.Color("Red"), To=pygame.Color("Blue"),
                                        Duration=0.5, Ease=EaseTypes.EaseOut)
        self.BorderColorAnimation.Play()
        self.FontColorAnimationValue = AnimatableValue(pygame.Color("Red"))
        self.FontColorAnimation = Animation(self.FontColorAnimationValue, From=pygame.Color("Red"), To=pygame.Color("Blue"),
                                        Duration=0.5, Ease=EaseTypes.EaseOut)
        self.FontColorAnimation.Play()

        #Initialize Default values and read config file/string
        self.defaultConfig = """
        position: 400,400           // Position X,Y (Center)                    [btn.x, btn.y]
        size: 150,100               // Size X,Y (From Center)                   [btn.sx, btn.sy]
        color: #263238              // Color Hex/Name                           [btn.maincolor, current color = btn.color]
        hovercolor: #A911BD         // Color on mouse hover                     [btn.hovercolor]
        clickedcolor: #A911BD       // Color on click                           [btn.clickedcolor]
        rounded: True               // Rounded corners                          [btn.rounded]
        radius: 30                  // Corner radius                            [btn.radius]
        bordered: True              // Bordered rect                            [btn.bordered]
        bordersize: 10              // Border width                             [btn.bordersize]
        bordercolor: #1E282D        // Border color                             [btn.mainbordercolor, current color=btn.bordercolor]
        borderhovercolor: #7C13A8   // Border color on hover                    [btn.borderhovercolor]
        borderclickedcolor: #A892DF // Border color on click                    [btn.borderclickedcolor]
        hidden: False               // Hide Button                              [btn.hidden]
        responsive: True            // Reacts to movement/clicks                [btn.responsive]
        nonresponsivecolor: #3E4B50 // Color when responsive = False            [btn.nonresponsivecolor]
        fontcolor: #A911BD          // Font color (Textcolor)                   [btn.mainfontcolor, current color = btn.fontcolor]
        fonthovercolor: #1C1C2B     // Font color on hover                      [btn.fonthovercolor]
        fontclickedcolor: #1C1C2B   // Font color on click                      [btn.fontclickedcolor]
        """

        self.ApplyConfig(self.defaultConfig)

        if len(args) == 5:
            self.x = args[0]            # X Position
            self.y = args[1]            # Y Position
            self.sx = args[2]           # X Size
            self.sy = args[3]           # Y Size
            self.color = args[4]        # Button Color
        elif len(args) == 1:
            self.ApplyConfig(args[0])
            self.label = Label("Heloo, am snek", "Arial", 30, self.x, self.y, "#A911BD")

        #Initialize Default Font
        self.SetFont("Arial", 30)
        self.label.align = 2

    def ApplyConfig(self, config):
        tc = config.split("\n")
        for value in tc:
            if ":" in value:
                k = value.split(":")[0].replace(" ", "").replace("\t", "")
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
                    self.color = AnimatableValue(pygame.Color(str(v)))
                    self.maincolor = pygame.Color(str(v))
                    self.ColorAnimation.From = self.maincolor
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
                    self.BorderColorAnimation.From = self.maincolor
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
                elif k == "fontcolor":
                    self.fontcolor = pygame.Color(v)
                    self.mainfontcolor = pygame.Color(v)
                    self.FontColorAnimation.From = self.maincolor
                elif k == "fonthovercolor":
                    self.fonthovercolor = pygame.Color(v)
                elif k == "fontclickedcolor":
                    self.fontclickedcolor = pygame.Color(v)

    def SetFont(self, font, fontsize):
        self.label.SetFont(font, fontsize)

    def PUIL_SetAnimation(self, To):
        if not self.ColorAnimation.To == To:
            self.ColorAnimation.From = self.color
            self.ColorAnimation.CurrentTime = 0
            self.ColorAnimation.PercentageComplete = 0
            self.ColorAnimation.Play()
        self.ColorAnimation.To = To

    def PUIL_SetBorderAnimation(self, To):
        if not self.BorderColorAnimation.To == To:
            self.BorderColorAnimation.From = self.BorderColorAnimationValue.value
            self.BorderColorAnimation.CurrentTime = 0
            self.BorderColorAnimation.PercentageComplete = 0
            self.BorderColorAnimation.Play()
        self.BorderColorAnimation.To = To

    def PUIL_SetFontAnimation(self, To):
        if not self.FontColorAnimation.To == To:
            self.FontColorAnimation.From = self.FontColorAnimationValue.value
            self.FontColorAnimation.CurrentTime = 0
            self.FontColorAnimation.PercentageComplete = 0
            self.FontColorAnimation.Play()
        self.FontColorAnimation.To = To

    def Draw(self, surface, fps = 60):
        self.label.x = self.x
        self.label.y = self.y
        self.label.text = self.text
        self.ColorAnimation.Update(fps)
        self.BorderColorAnimation.Update(fps)
        self.FontColorAnimation.Update(fps)
        self.color = self.ColorAnimationValue.value
        self.label.color = self.FontColorAnimationValue.value
        if self.responsive:
            mpos = pygame.mouse.get_pos()
            if mpos[0] > self.x-self.sx/2 and mpos[0] < self.x+self.sx/2 and mpos[1] > self.y-self.sy/2 and \
                                                                                    mpos[1] < self.y+self.sy/2:
                if pygame.mouse.get_pressed(3)[0]:
                    self.PUIL_SetAnimation(self.clickedcolor)
                    self.PUIL_SetBorderAnimation(self.borderclickedcolor)
                    self.PUIL_SetFontAnimation(self.fontclickedcolor)
                    if hasattr(self, 'func') and not self.hidden:
                        if hasattr(self, "args") and not self.args == None:
                            self.func(self.args)
                        self.func()
                else:
                    self.PUIL_SetAnimation(self.hovercolor)
                    self.PUIL_SetBorderAnimation(self.borderhovercolor)
                    self.PUIL_SetFontAnimation(self.fonthovercolor)
            else:
                self.PUIL_SetAnimation(self.maincolor)
                self.PUIL_SetBorderAnimation(self.mainbordercolor)
                self.PUIL_SetFontAnimation(self.mainfontcolor)
        else:
            self.PUIL_SetAnimation(self.nonresponsivecolor)
            self.PUIL_SetBorderAnimation(self.nonresponsivecolor)
            self.PUIL_SetFontAnimation(self.nonresponsivecolor)
        if not self.hidden:
            if not self.rounded:
                if not self.bordered:
                    pygame.draw.rect(surface, self.ColorAnimationValue.value,
                                    pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy))
                else:
                    pygame.draw.rect(surface, self.BorderColorAnimationValue.value,
                                    pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy))
                    pygame.draw.rect(surface, self.ColorAnimationValue.value, pygame.Rect(
                                    self.x-self.sx/2+self.bordersize,
                                    self.y-self.sy/2+self.bordersize,
                                    self.sx-self.bordersize*2,
                                    self.sy-self.bordersize*2))
            else:
                if not self.bordered:
                    draw_rounded_rect(surface, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy),
                                        self.ColorAnimationValue.value, self.radius)
                else:
                    draw_bordered_rounded_rect(surface, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy),
                            self.ColorAnimationValue.value, self.BorderColorAnimationValue.value, self.radius, self.bordersize)
        self.label.Draw(surface)

    def SetFunction(self, func, args = None):
        self.func = func
        self.args = args

class Label():
    def __init__(self, *args):

        self.defaultConfig = """
        position: 250,475
        fontcolor: #A911BD
        hidden: False
        align: Center
        """

        self.SetFont("Arial", 30)
        self.isttf = False
        self.height = 1
        self.width = 1
        self.hidden = False
        self.align = 0
        self.ApplyConfig(self.defaultConfig)
        if len(args) == 1:
            self.x = 0
            self.y = 0
            self.sx = 100
            self.sy = 100
            self.color = pygame.Color("Red")
            self.align = 0
            self.ApplyConfig(args[0])
        elif len(args) == 6:
            if args[1]+"."+str(args[2]) not in loadedFonts:
                PreloadFont(args[1], args[2])
            self.tfont = loadedFonts[args[1]+"."+str(args[2])]
            self.text = args[0]
            self.x = args[3]
            self.y = args[4]
            self.color = pygame.Color(args[5])

    def ApplyConfig(self, config):
        tc = config.split("\n")
        for value in tc:
            if ":" in value:
                k = value.split(":")[0].replace(" ", "").replace("\t", "")
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

    def SetFont(self, font, fontsize):
        if font+"."+str(fontsize) not in loadedFonts:
            PreloadFont(font, fontsize)
        self.isttf = False
        if ".ttf" in font:
            font = font.replace(".ttf", "")
            self.isttf = True
        self.tfont = loadedFonts[font+"."+str(fontsize)]

    def Draw(self, surface, fps = 60):
        if not self.hidden:
            if not self.isttf:
                text_surface = self.tfont.render(self.text, False, self.color)
            else:
                text_surface, r = self.tfont.render(text=self.text, fgcolor=self.color)
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
                k = value.split(":")[0].replace(" ", "").replace("\t", "")
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
        if Distance(int((self.x-self.width/2)+self.value*(self.width/self.max)), pygame.mouse.get_pos()[0], self.y,
                        pygame.mouse.get_pos()[1]) <= self.knobsize:
            if self.responsive:
                if pygame.mouse.get_pressed(3)[0]:
                    if not PUIL_CursorDragging:
                        self.dragging = True
                        PUIL_CursorDragging = True
        if self.dragging:
            if pygame.mouse.get_pressed(3)[0] == False:
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
        draw_rounded_rect(surface, pygame.Rect(self.x-self.width/2-self.knobsize+4,
                            int(self.y-self.linesize/2), self.width+self.knobsize*2-8,
        int(self.linesize)), self.linecolor, int(math.floor(self.linesize/2)-2))
        draw_circle(surface, int((self.x-self.width/2)+self.value*(self.width/self.max)),
                                int(self.y), self.knobsize, self.knobcolor)

class InputField():
    def __init__(self, config = None):
        #Initialize Animations


        #Initialize Assistant UIElements
        self.label = Label()
        self.label.align = 0
        self.text = ""
        self.active = True

        #Initialize Default values and read config file/string
        self.defaultConfig = """
        position: 400,400
        width: 300
        color: #263238
        hidden: False
        responsive: True
        nonresponsivecolor: #3E4B50
        placeholdercolor: #28283D
        """
        self.placeholder = "Enter text..."

        self.ApplyConfig(self.defaultConfig)
        if not config == None:
            self.ApplyConfig(config)

        self.label.SetFont("Fonts/Roboto-Thin.ttf", 30)

    def ApplyConfig(self, config):
        tc = config.split("\n")
        for value in tc:
            if ":" in value:
                k = value.split(":")[0].replace(" ", "").replace("\t", "")
                v = value.split(":")[1].replace(" ", "").replace("\t", "")
                if "//" in v :
                    v = v.split("//")[0]
                if k == "position":
                    self.x = int(v.split(",")[0])
                    self.y = int(v.split(",")[1])
                elif k == "width":
                    self.width = int(v)
                elif k == "color":
                    self.color = AnimatableValue(pygame.Color(str(v)))
                    self.maincolor = pygame.Color(str(v))
                elif k == "hidden":
                    self.hidden = v == "True"
                elif k == "responsive":
                    self.responsive = v == "True"
                elif k == "nonresponsivecolor":
                    self.nonresponsivecolor = pygame.Color(v)
                elif k == "placeholdercolor":
                    self.placeholdercolor = pygame.Color(v)

    def SetPlaceholder(self, p):
        self.placeholder = p

    def UpdateEventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def Draw(self, surface, fps = 60):
        self.label.x = self.x-self.width/2+5
        self.label.y = self.y
        if not self.active:
            self.label.text = self.placeholder
            self.label.color = self.placeholdercolor
        else:
            self.label.text = self.text
            self.label.color = self.maincolor
        self.label.Draw(surface, fps)
        draw_rounded_rect(surface, pygame.Rect(self.x-self.width/2, self.y+20, self.width, 6), self.maincolor, 2)


print("[PygameUILib] Done!")
print()
