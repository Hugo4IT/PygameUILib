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
def GetByID(address):
    return [x for x in globals().values() if id(x)==address]

def Lerp(A, B, C):
    return (C * A) + ((1-C) * B)

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

    def Stop(self):
        self.Playing = False

    def Update(self, fps = 60):
        if self.Playing:
            self.CurrentTime += self.Duration / fps
            print("CT"+str(self.CurrentTime))
            self.PercentageComplete = max(self.CurrentTime / self.Duration,1.0)
            self.AnimValue.value = numpy.interp(self.From, self.To, self.PercentageComplete);
            print("PC"+str(self.PercentageComplete))
            print("AV"+str(self.AnimValue.value))
            if self.Step is not None:
                self.Step()
