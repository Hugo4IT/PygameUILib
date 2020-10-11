import math
import pygame

class Player:
    global PColor
    global PWidth
    global PHeight
    PColor = pygame.Color("Red")
    PWidth = 50
    PHeight = 120
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.rotation = 0

    def Draw(self, surface):
        # Sin X, Cos Y
        rRadians = math.radians(self.rotation)

        bottomLeft = rotate((self.x, self.y), (self.x-PWidth/2, self.y+PHeight/2), rRadians)
        topLeft = rotate((self.x, self.y), (self.x-PWidth/2, self.y-PHeight/2), rRadians)
        bottomRight = rotate((self.x, self.y), (self.x+PWidth/2, self.y+PHeight/2), rRadians)
        topRight = rotate((self.x, self.y), (self.x+PWidth/2, self.y-PHeight/2), rRadians)

        pygame.draw.aaline(surface, PColor, bottomLeft, topLeft) # Left
        pygame.draw.aaline(surface, PColor, bottomRight, topRight) # Right
        pygame.draw.aaline(surface, PColor, bottomRight, bottomLeft) # Bottom
        pygame.draw.aaline(surface, PColor, topLeft, topRight) # Top

    def Forward(self, amount):
        rRadians = math.radians(self.rotation)
        point = rotate((self.x, self.y), (self.x, self.y - amount), rRadians)
        self.x = point[0]
        self.y = point[1]

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
