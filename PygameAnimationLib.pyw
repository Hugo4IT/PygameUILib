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
    return A + C * (B - A)

def EaseIn(a):
    return a*a

class EaseTypes(Enum):
    NONE = 1
    EaseIn = 2
    EaseOut = 3
    EaseInOut = 4

class AnimatableValue:
    def __init__(self, value = 0):
        self.value = value

class Animation:
    def __init__(self, value, Duration = 1, From = 0, To = 100, Ease = EaseTypes.NONE, Loop = False, OnStart = None, Step = None, OnEnd = None):
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

    def Play(self):
        self.Playing = True
        if self.OnStart is not None:
            self.OnStart()

    def Stop(self):
        self.Playing = False
        if self.OnEnd is not None:
            self.OnEnd()

    def Update(self, fps = 60):
        if self.Playing:
            self.CurrentTime += self.Duration / fps
            self.PercentageComplete = numpy.clip(self.CurrentTime / self.Duration, 0.0, 1.0)
            self.AnimValue.value = numpy.clip(Lerp(self.From, self.To, EaseIn(self.PercentageComplete)), self.From, self.To)
            if self.Step is not None:
                self.Step()
            if self.PercentageComplete == 1.0:
                if self.Loop == True:
                    self.CurrentTime = 0
                    self.PercentageComplete = 0.0
                else:
                    self.Stop()
