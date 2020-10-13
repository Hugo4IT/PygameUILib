from PygameUI import *

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
        self.align = 2

    def Draw(self, surface):
        text_surface = self.tfont.render(self.text, False, self.color)
        self.height = text_surface.get_height()
        self.width = text_surface.get_width()
        if self.align == 2:
            surface.blit(text_surface, (self.x-self.width/2, self.y-self.height/2))
