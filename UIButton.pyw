from PygameUI import loadedFonts, PreloadFont, draw_rounded_rect, draw_bordered_rounded_rect
from UILabel import *

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
            self.label = Label("Heloo, am snek", "Arial", 30, self.x, self.y, "Red")

    def Draw(self, surface):
        if self.responsive:
            mpos = pygame.mouse.get_pos()
            if mpos[0] > self.x-self.sx/2 and mpos[0] < self.x+self.sx/2 and mpos[1] > self.y-self.sy/2 and mpos[1] < self.y+self.sy/2:
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
