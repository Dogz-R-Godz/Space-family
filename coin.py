import pygame as pg
from imageImporter import images
import random as rand
import player as pla
import math as maths

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

class coin:
    def __init__(self, pos, cashAmount, screen:pg.Surface):
        self.pos=pos
        self.internalTimer=0
        self.cashAmount=cashAmount
        self.velo=(0, 0)
        self.sprites=images["Projectiles"]["CashPellet"]
        self.currSprite=self.sprites[0]
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.fuckOff=False
        self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.screen=screen
    def update(self, player: pla.player): 
        self.internalTimer+=1

        posDifference=(player.pos[0]-self.pos[0], player.pos[1]-self.pos[1])

        posDiffSum=abs(posDifference[0])+abs(posDifference[1])

        posDifference2=(posDifference[0]/posDiffSum, posDifference[1]/posDiffSum)

        self.velo=(clamp(self.velo[0]+posDifference2[0], -4, 4), clamp(self.velo[1]-posDifference2[1], -4, 4))

        self.pos=(self.pos[0] + self.velo[0], self.pos[1] - self.velo[1])
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
        #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])

            
        if player.rect.colliderect(self.rect):
            self.fuckOff=True
            player.cash+=self.cashAmount
        
    
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))
