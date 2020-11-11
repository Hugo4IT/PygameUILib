#Libraries
import sys
import pygame
import pygame.freetype
from pygame.locals import *

#Classes & Variables
from Player import Player           #Player Class
from Settings import *              #Settings Variables
from PygameUILib import *           #UI Classes

print("Pygame Init()")
pygame.init()

print("Capping FPS...")
fps = 60
fpsClock = pygame.time.Clock()

print("Creating Screen")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

print("Creating Player")
p = Player(200, 200)
objects = []
objects.append(p)

bgColor1 = AnimatableValue(0)
bgColor2 = 0
bgColor3 = 0
anim = Animation(bgColor1, Duration=2, From=0, To=255, Loop=True)
anim.Play()

btnConfig = """
position: 400,400           // Position X,Y (Center)                    [btn.x, btn.y]
size: 300,100               // Size X,Y (From Center)                   [btn.sx, btn.sy]
color: #263238              // Color Hex/Name                           [btn.maincolor, current color = btn.color]
hovercolor: #303C42         // Color on mouse hover                     [btn.hovercolor]
clickedcolor: #A911BD       // Color on click                           [btn.clickedcolor]
rounded: True               // Rounded corners                          [btn.rounded]
radius: 30                  // Corner radius                            [btn.radius]
bordered: True              // Bordered rect                            [btn.bordered]
bordersize: 10              // Border width                             [btn.bordersize]
bordercolor: #1E282D        // Border color                             [btn.mainbordercolor, current border color = btn.bordercolor]
borderhovercolor: #E7E5F1   // Border color on hover                    [btn.borderhovercolor]
borderclickedcolor: #A892DF // Border color on click                    [btn.borderclickedcolor]
hidden: False               // Hide Button                              [btn.hidden]
responsive: True            // Reacts to movement/clicks                [btn.responsive]
nonresponsivecolor: #3E4B50 // Color when responsive = False            [btn.nonresponsivecolor]
fontpath: Arial             // Path to font or name of system font      [NOT IMPLEMENTED]
fontcolor: #FFFFFF          // Font color (Textcolor)                   [NOT IMPLEMENTED]
fontsize: auto              // Size of font (can be int or auto)        [NOT IMPLEMENTED]
"""

labelConfig = """
font: Arial
fontsize: 30
position: 500,500
fontcolor: #037CD6
hidden: False
"""

print("Creating Button and Label")
btnTest = Button(btnConfig)
labelTest = Label("THAT WAS LEGITNESS", "Arial", 30, 500, 500, "Red")

def QuitGame():
    pygame.quit()
    sys.exit()

btnTest.SetFunction(QuitGame)

# Game loop.
while True:
    anim.Update()
    screen.fill((bgColor1.value, bgColor2, bgColor3))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                btnTest.hidden = not btnTest.hidden
    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_LEFT]:
        p.rotation -= 4
    if key_input[pygame.K_UP]:
        p.Forward(8)
    if key_input[pygame.K_RIGHT]:
        p.rotation += 4
    if key_input[pygame.K_DOWN]:
        p.Forward(-8)

    p.Draw(screen)
    btnTest.Draw(screen)
    labelTest.Draw(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
