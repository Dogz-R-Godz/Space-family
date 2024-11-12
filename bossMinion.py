import pygame as pg
from pygame import mixer
from imageImporter import images
import math as maths
import random as rand
import player as pla
from bullet import bossBullet

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

class bossMinion:
    def __init__(self, pos, endingPos, shotCooldown, accuracy, bulletDamage, bulletLifespan, movementTime, fps, screen:pg.Surface):
        self.pos=pos
        self.startingPos=pos
        self.fps=fps
        self.shotCooldown=shotCooldown
        self.accuracy=accuracy
        self.bulletDamage=bulletDamage
        self.bulletLifespan=bulletLifespan
        self.screen=screen
        self.sprites=images["Boss"]["minion"]
        self.currSprite=self.sprites[0]
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.rotation=0
        self.currCooldown=0
        self.movementTime=movementTime
        self.currMovementTime=movementTime
        self.internalTimer=0
        self.finalPos=endingPos
        self.fuckOff=False
        self.velo=((self.finalPos[0]-self.startingPos[0])/(self.movementTime*fps), (self.finalPos[1]-self.startingPos[1])/(self.movementTime*fps))
    def updateSprite(self):
        if self.internalTimer%10 == 0:
            self.currSprite = self.sprites[0]
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation+180)
            self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
    def update(self, player:pla.player, bossBullets):
        self.internalTimer+=1
        speedMultiplier=120/self.fps
        if self.currMovementTime >= 0:
            self.velo=((self.startingPos[0]-self.finalPos[0])/(self.movementTime*self.fps), (self.startingPos[1]-self.finalPos[1])/(self.movementTime*self.fps))
            currFrameVelo=(self.velo[0], self.velo[1])
            self.pos = (self.pos[0]-currFrameVelo[0], self.pos[1]-currFrameVelo[1])
            self.currMovementTime -= 1/self.fps
        else:
            self.currCooldown-=1

            posDifference=(self.pos[0]-player.pos[0], self.pos[1]-player.pos[1])


            self.rotation=maths.degrees(maths.atan2(posDifference[1], -posDifference[0]))+90 if posDifference[0] != 0 else 0

            
            if self.currCooldown <= 0:
                self.currCooldown=self.shotCooldown*speedMultiplier
                rotation=maths.degrees(maths.atan2((self.pos[1]-player.pos[1]), -(self.pos[0]-player.pos[0])))+90 if (self.pos[0]-player.pos[0]) != 0 else 0
                #rotation=0-rotation

                rotation+=((2*rand.random())-1)*self.accuracy
                xAdder1=maths.sin(maths.radians(rotation+180))
                yAdder1=maths.cos(maths.radians(rotation+180))
                bossBullets.append(bossBullet(self.pos, (-xAdder1, yAdder1), rotation, self.bulletDamage, self.bulletLifespan, "BossBullet", 1, self.fps, self.screen))

            self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.updateSprite()
    def die(self):
        self.fuckOff=True
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))