import AnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import random

class CakeAnimatedProp(AnimatedProp.AnimatedProp):

    def __init__(self, node):
        AnimatedProp.AnimatedProp.__init__(self, node)
        parent = node.getParent()
        self.cake = Actor.Actor(node, copy=0)
        self.cake.reparentTo(parent)
        self.cake.loadAnims({'flames': 'phase_5/models/props/birthday-cake-chan'})
        self.cake.pose('flames', 0)
        self.node = self.cake

    def delete(self):
        AnimatedProp.AnimatedProp.delete(self)
        self.cake.cleanup()
        del self.cake
        del self.node

    def enter(self):
        AnimatedProp.AnimatedProp.enter(self)
        self.cake.loop('flames')

    def exit(self):
        AnimatedProp.AnimatedProp.exit(self)
        self.cake.stop()