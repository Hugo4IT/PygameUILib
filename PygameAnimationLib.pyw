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
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

print("[PygameAnimationLib] Loading PygameAnimationLib...")
def GetID(address):
    return [x for x in globals().values() if id(x)==address]

class Animation:
    def __init__(self, value, OnStart = None, Step = None, OnEnd = None):
        self.ID = id(value)
        self.OnStart = OnStart
        self.Step = Step
        self.OnEnd = OnEnd

    def Play(self):
        pass

    def Pause(self):
        pass

    def Stop(self):
        pass
