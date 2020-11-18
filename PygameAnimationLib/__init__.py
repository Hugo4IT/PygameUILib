print("""
#===================================================#
#                                                   #
#   Title: PygameAnimationLib                       #
#   Author: Hugo van de Kuilen from Hugo4IT         #
#   Website: Hugo4IT.com                            #
#                                                   #
#===================================================#
""")

print("[PygameAnimationLib] Loading Libraries...")
import os
import math
import numpy
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from enum import Enum

print("[PygameAnimationLib] Loading PygameAnimationLib...")
def GetByID(ID):
    return [x for x in globals().values() if id(x)==ID]

def Lerp(A, B, C):
    if not type(A) == type(B):
        if not type(A) == numpy.ndarray:
            print("Error: Animation.From and Animation.To must be the same type")
            print("Type of Animation.From: "+str(type(A)))
            print("Type of Animation.To: "+str(type(B)))
    if type(A) == pygame.Color:
        result = CLerp(A, B, C)
    else:
        result = A + C * (B - A)
    return result

def CLerp(A, B, C):
    return pygame.Color(int(Lerp(A.r, B.r, C)),int(Lerp(A.g, B.g, C)), int(Lerp(A.b, B.b, C)))

def EaseIn(x):
    return x*x*x

def EaseOut(x):
    return 1 - math.pow(1 - x, 3)

def EaseInOut(x):
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 3) / 2

class EaseTypes(Enum):
    NONE = 1
    EaseIn = 2
    EaseOut = 3
    EaseInOut = 4

class AnimatableValue:
    def __init__(self, value = 0):
        self.value = value

class Animation:
    def __init__(self, value, Duration = 1, From = 100, To = 0, Ease = EaseTypes.NONE,
                Loop = False, OnStart = None, Step = None, OnEnd = None, LoopReverse = True):
        self.AnimValue = value
        self.OnStart = OnStart
        self.Step = Step
        self.OnEnd = OnEnd
        self.Ease = Ease
        self.Loop = Loop
        self.From = From
        self.To = To
        self.Duration = Duration
        self.CurrentTime = 0
        self.PercentageComplete = 0
        self.Playing = False
        self.R = False
        self.LoopReverse = LoopReverse

    def Play(self):
        self.Playing = True
        if self.OnStart is not None:
            self.OnStart()
        return self

    def Stop(self):
        self.Playing = False
        if self.OnEnd is not None:
            self.OnEnd()
        self.CurrentTime = 0
        self.PercentageComplete = 0

    def Restart(self):
        self.Stop()
        self.Play()

    def Update(self, fps = 60):
        if self.Playing:
            if fps > 3:
                self.CurrentTime += 1 / fps
            else:
                self.CurrentTime += 0.01
            self.PercentageComplete = numpy.clip(self.CurrentTime / self.Duration, 0.0, 1.0)
            if self.Ease == EaseTypes.NONE:
                self.AnimValue.value = Lerp(self.From, self.To, self.PercentageComplete)
            elif self.Ease == EaseTypes.EaseIn:
                self.AnimValue.value = Lerp(self.From, self.To, EaseIn(self.PercentageComplete))
            elif self.Ease == EaseTypes.EaseOut:
                self.AnimValue.value = Lerp(self.From, self.To, EaseOut(self.PercentageComplete))
            elif self.Ease == EaseTypes.EaseInOut:
                self.AnimValue.value = Lerp(self.From, self.To, EaseInOut(self.PercentageComplete))
            if self.R:
                self.AnimValue.value = self.To - self.AnimValue.value
            if self.Step is not None:
                self.Step()
            if self.PercentageComplete == 1.0:
                if self.Loop == True:
                    self.CurrentTime = 0
                    self.PercentageComplete = 0.0
                    if self.LoopReverse:
                        self.R = not self.R
                else:
                    self.Stop()
