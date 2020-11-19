#Libraries
import sys
import pygame
import pygame.freetype
from pygame.locals import *
from screeninfo import get_monitors

#Classes & Variables
from PygameUILib import *           #UI Classes

screensize = (1920, 1080)

for m in get_monitors():
    screensize = m.width, m.height

print("Pygame Init()")
pygame.init()

print("Capping FPS...")
fps = 60
fpsClock = pygame.time.Clock()

print("Creating Screen")
Fullscreen = True
screen = pygame.display.set_mode(screensize, pygame.FULLSCREEN)
if not Fullscreen:
    screen = pygame.display.set_mode(screensize, pygame.NOFRAME)

btnConfig = """
position: 400,400           // Position X,Y (Center)                    [btn.x, btn.y]
size: 150,100               // Size X,Y (From Center)                   [btn.sx, btn.sy]
color: #263238              // Color Hex/Name                           [btn.maincolor, current color = btn.color]
hovercolor: #A911BD         // Color on mouse hover                     [btn.hovercolor]
clickedcolor: #A911BD       // Color on click                           [btn.clickedcolor]
rounded: True               // Rounded corners                          [btn.rounded]
radius: 30                  // Corner radius                            [btn.radius]
bordered: True              // Bordered rect                            [btn.bordered]
bordersize: 10              // Border width                             [btn.bordersize]
bordercolor: #1E282D        // Border color                             [btn.mainbordercolor, current border color = btn.bordercolor]
borderhovercolor: #7C13A8   // Border color on hover                    [btn.borderhovercolor]
borderclickedcolor: #A892DF // Border color on click                    [btn.borderclickedcolor]
hidden: False               // Hide Button                              [btn.hidden]
responsive: True            // Reacts to movement/clicks                [btn.responsive]
nonresponsivecolor: #3E4B50 // Color when responsive = False            [btn.nonresponsivecolor]
fontcolor: #A911BD          // Font color (Textcolor)                   [btn.mainfontcolor, current color = btn.fontcolor]
fonthovercolor: #1C1C2B     // Font color on hover                      [btn.fonthovercolor]
fontclickedcolor: #1C1C2B   // Font color on click                      [btn.fontclickedcolor]
"""

labelConfig = """
position: 250,475
fontcolor: #A911BD
hidden: False
align: Center
"""

inputFieldConfig = """
position: 250,550
width: 300
color: #A911BD
hidden: False
"""

sliderLabelConfig = """
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

SliderConfig2 = """
position: 900, 800
linecolor: #28283D
knobcolor: #A911BD
width: 300
linesize: 60
knobsize: 30
value: 0
max: 100
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
l1 = Label(sliderLabelConfig)
l1.y = 100
l1.SetFont("Fonts/Roboto-Thin.ttf", 40)
l1.text = "None (Linear)"
uielems.append(l1)
l2 = Label(sliderLabelConfig)
l2.y = 200
l2.text = "Ease In"
l2.SetFont("Fonts/Roboto-Thin.ttf", 40)
uielems.append(l2)
l3 = Label(sliderLabelConfig)
l3.y = 300
l3.SetFont("Fonts/Roboto-Thin.ttf", 40)
l3.text = "Ease Out"
uielems.append(l3)
l4 = Label(sliderLabelConfig)
l4.y = 400
l4.SetFont("Fonts/Roboto-Thin.ttf", 40)
l4.text = "Ease In & Out"
uielems.append(l4)
l5 = Label(labelConfig)
l5.SetFont("Fonts/Roboto-Thin.ttf", 40)
l5.text = "Slider: 2s Animation"
uielems.append(l5)
l6 = Label(labelConfig)
l6.SetFont("Fonts/Roboto-Thin.ttf", 40)
l6.text = "FPS: 999"
l6.x = 50
l6.align = 0
l6.y = screen.get_height() - 50
uielems.append(l6)

#Styles Demo UI Elements
s5 = Slider(SliderConfig2)
s5.y = 100
s5.value = 66
uielems.append(s5)
s6 = Slider(SliderConfig2)
s6.y = 200
s6.knobsize = 15
s6.linesize = 6
uielems.append(s6)
s7 = Slider(SliderConfig2)
s7.y = 300
s7.knobcolor = pygame.Color("#2a4151")
s7.linecolor = pygame.Color("#83f7a0")
s7.value = 33
uielems.append(s7)
s8 = Slider(SliderConfig2)
s8.y = 400
s8.value = 100
uielems.append(s8)

print("Creating Animations")
animations = []
NoEasingValue = AnimatableValue(0)
NoEasing = Animation(NoEasingValue, From = 0, To = 100, Duration = 2, Ease = EaseTypes.NONE, Loop = True, LoopReverse = True)
animations.append(NoEasing)
EaseInValue = AnimatableValue(0)
EaseIn = Animation(EaseInValue, From = 0, To = 100, Duration = 2, Ease = EaseTypes.EaseIn, Loop = True, LoopReverse = True)
animations.append(EaseIn)
EaseOutValue = AnimatableValue(0)
EaseOut = Animation(EaseOutValue, From = 0, To = 100, Duration = 2, Ease = EaseTypes.EaseOut, Loop = True, LoopReverse = True)
animations.append(EaseOut)
EaseInOutValue = AnimatableValue(0)
EaseInOut = Animation(EaseInOutValue, From = 0, To = 100, Duration = 2, Ease = EaseTypes.EaseInOut, Loop = True, LoopReverse = True)
animations.append(EaseInOut)
for a in animations:
    a.Play()

def QuitGame():
    pygame.quit()
    sys.exit()

btnAnimationTest = Button(btnConfig)
btnAnimationTest.y = 600
btnAnimationTest.SetFont("Fonts/Roboto-Thin.ttf", 40)
btnAnimationTest.SetFunction(QuitGame)
btnAnimationTest.text = "Quit"
uielems.append(btnAnimationTest)

ifTest = InputField(inputFieldConfig)
uielems.append(ifTest)

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

    s1.value = NoEasingValue.value
    s2.value = EaseInValue.value
    s3.value = EaseOutValue.value
    s4.value = EaseInOutValue.value

    tfps = fpsClock.get_fps()
    if tfps < 3:
        tfps = 3
    l6.text = "FPS: "+str(int(tfps))

    for a in animations:
        a.Update(int(tfps))

    for e in uielems:
        e.Draw(screen, int(tfps))

    pygame.display.flip()
    fpsClock.tick(fps)
