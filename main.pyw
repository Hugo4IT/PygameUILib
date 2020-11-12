#Libraries
import sys
import pygame
import pygame.freetype
from pygame.locals import *

#Classes & Variables
from PygameUILib import *           #UI Classes

print("Pygame Init()")
pygame.init()

print("Capping FPS...")
fps = 60
fpsClock = pygame.time.Clock()

print("Creating Screen")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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
fontcolor: #FFFFFF          // Font color (Textcolor)                   [NOT IMPLEMENTED]
"""

labelConfig = """
position: 450,500
fontcolor: #A911BD
hidden: False
align: Left
"""

SliderConfig = """
position: 250, 800
linecolor: #28283D
knobcolor: #A911BD
width: 300
linesize: 60
knobsize: 30
value: 0
max: 100
responsive: False
"""

print("Initializing User Interface Elements")
#AnimationLib Demo UI Elements
uielems = []
s1 = Slider(SliderConfig)
s1.y = 100
uielems.append(s1)
s2 = Slider(SliderConfig)
s2.y = 200
uielems.append(s2)
s3 = Slider(SliderConfig)
s3.y = 300
uielems.append(s3)
s4 = Slider(SliderConfig)
s4.y = 400
uielems.append(s4)
l1 = Label(labelConfig)
l1.y = 100
l1.SetFont("Arial.30")
l1.text = "None (Linear)"
uielems.append(l1)
l2 = Label(labelConfig)
l2.y = 200
l2.text = "Ease In"
l2.SetFont("Arial.30")
uielems.append(l2)
l3 = Label(labelConfig)
l3.y = 300
l3.SetFont("Arial.30")
l3.text = "Ease Out"
uielems.append(l3)
l4 = Label(labelConfig)
l4.y = 400
l4.SetFont("Arial.30")
l4.text = "Ease In & Out"
uielems.append(l4)

print("Creating Animations")
animations = []
NoEasingValue = AnimatableValue(0)
NoEasing = Animation(NoEasingValue, From = 0, To = 100, Duration = 3, Ease = EaseTypes.NONE)
animations.append(NoEasing)
EaseInValue = AnimatableValue(0)
EaseIn = Animation(EaseInValue, From = 0, To = 100, Duration = 3, Ease = EaseTypes.EaseIn)
animations.append(EaseIn)
EaseOutValue = AnimatableValue(0)
EaseOut = Animation(EaseOutValue, From = 0, To = 100, Duration = 3, Ease = EaseTypes.EaseOut)
animations.append(EaseOut)
EaseInOutValue = AnimatableValue(0)
EaseInOut = Animation(EaseInOutValue, From = 0, To = 100, Duration = 3, Ease = EaseTypes.EaseInOut)
animations.append(EaseInOut)
for a in animations:
    a.Play()
RNoEasingValue = AnimatableValue(100)
RNoEasing = Animation(RNoEasingValue, From = 100, To = 0, Duration = 3, Ease = EaseTypes.NONE)
animations.append(RNoEasing)
REaseInValue = AnimatableValue(100)
REaseIn = Animation(REaseInValue, From = 100, To = 0, Duration = 3, Ease = EaseTypes.EaseIn)
animations.append(REaseIn)
REaseOutValue = AnimatableValue(100)
REaseOut = Animation(REaseOutValue, From = 100, To = 0, Duration = 3, Ease = EaseTypes.EaseOut)
animations.append(REaseOut)
REaseInOutValue = AnimatableValue(100)
REaseInOut = Animation(REaseInOutValue, From = 100, To = 0, Duration = 3, Ease = EaseTypes.EaseInOut)
animations.append(REaseInOut)

def SetRev():
    global Reverse
    Reverse = True
    RNoEasing.Play()

NoEasing.OnEnd = SetRev
EaseIn.OnEnd = REaseIn.Play
EaseOut.OnEnd = REaseOut.Play
EaseInOut.OnEnd = REaseInOut.Play
RNoEasing.OnEnd = NoEasing.Play
REaseIn.OnEnd = EaseIn.Play
REaseOut.OnEnd = EaseOut.Play
REaseInOut.OnEnd = EaseInOut.Play

def QuitGame():
    pygame.quit()
    sys.exit()

global Reverse
Reverse = False

# Game loop.
while True:
    screen.fill(pygame.Color("#1C1C2B"))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                QuitGame()
    key_input = pygame.key.get_pressed()

    if EaseInValue.value == 100:
        Reverse = True
        EaseInValue.value = 0
    #if REaseInValue.value == 0:
    #    Reverse = False
    #    REaseInValue.value = 100

    if not Reverse:
        s1.value = RNoEasingValue.value
        s2.value = REaseInValue.value
        s3.value = REaseOutValue.value
        s4.value = REaseInOutValue.value
    else:
        s1.value = RNoEasingValue.value
        s2.value = REaseInValue.value
        s3.value = REaseOutValue.value
        s4.value = REaseInOutValue.value

    for a in animations:
        a.Update(fps)

    for e in uielems:
        e.Draw(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
