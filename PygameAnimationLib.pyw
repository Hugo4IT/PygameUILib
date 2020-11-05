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
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from enum import Enum

print("[PygameAnimationLib] Loading PygameAnimationLib...")
def GetID(address):
    return [x for x in globals().values() if id(x)==address]

class EaseTypes(Enum):
    NONE = 1
    EaseIn = 2
    EaseOut = 3
    EaseInOut = 4

class Animation:
    def __init__(self, value, Duration = 1, From = 0, To = 100, Ease = EaseTypes.NONE, Loop = False, OnStart = None, Step = None, OnEnd = None):
        self.ID = id(value)
        self.OnStart = OnStart
        self.Step = Step
        self.OnEnd = OnEnd
        self.Ease = Ease
        self.Loop = Loop
        self.From = From
        self.To = To
        self.Duration = Duration
        self.CurrentTime = 0

    def Play(self):
        pass

    def Stop(self):
        pass

    def Update(self, fps = 60):
        self.CurrentTime += self.Duration / fps
        if self.Step is not None:
            self.Step()
