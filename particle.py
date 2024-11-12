import pygame as pg

class particle:
    def __init__(self, pos, velo, interactable, colour, lifespan, fade, transparancy, fps, screen:pg.Surface):
        self.pos=pos
        self.velo=velo
        self.interactable=interactable
        self.colour=colour
        self.lifespan=lifespan
        self.currLifespan=lifespan
        self.fade=fade
        self.fps=fps
        self.screen=screen
        self.fuckOff=False
        self.transparancy=transparancy
        self.initTransparancy=transparancy
        self.surf=pg.Surface((5, 5))
        self.surf.set_alpha(transparancy)
    def update(self):
        self.currLifespan -= (1/self.fps)
        if self.currLifespan <= 0:
            self.fuckOff=True
        if self.fade:
            self.transparancy-=(self.initTransparancy/(self.lifespan*self.fps))
        self.pos = (self.pos[0]+self.velo[0], self.pos[1]+self.velo[1])
    def render(self):
        self.surf.set_alpha(self.transparancy)
        self.surf.fill(self.colour)
        self.screen.blit(self.surf, (self.pos[0] - 2.5, self.pos[1]-2.5))
        #self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))

