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

class bossMissile:
    def __init__(self, pos, speed, damage, rotation, lifespan, fps, screen:pg.Surface):
        self.pos=pos
        self.internalTimer=0
        self.fps=fps
        self.lifespan=lifespan
        self.velo=(0, 0)
        self.speed=speed*(120/self.fps)
        self.damage=damage
        self.rotation=rotation
        self.sprites=images["Projectiles"]["BossMissile"]
        self.currSprite=self.sprites[0]
        self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.fuckOff=False
        self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.screen=screen
    
    def updateSprite(self):
        if round(self.internalTimer*120)%10 == 0:
            self.currSprite = rand.choice(self.sprites)
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        


    
    def update(self, player: pla.player, playerBullets: list): 
        self.internalTimer+=(1/self.fps)

        #posDifference=(self.pos[0]-player.pos[0], self.pos[1]-player.pos[1])

        #posDiffSum=(posDifference[0]+posDifference[1])/(120/self.fps)

        #posDifference2=((posDifference[0]*4)/posDiffSum, (posDifference[1]*4)/posDiffSum)

        rotation=maths.degrees(maths.atan2((self.pos[1]-player.pos[1]), -(self.pos[0]-player.pos[0])))+90 if (self.pos[0]-player.pos[0]) != 0 else 0

        xAdder=maths.sin(maths.radians(rotation))*(self.speed/2)*(120/self.fps)
        yAdder=maths.cos(maths.radians(rotation))*(self.speed/2)*(120/self.fps)

        self.rotation=rotation

        self.velo=(clamp(self.velo[0]+xAdder, -self.speed, self.speed), clamp(self.velo[1]+yAdder, -self.speed, self.speed))

        self.pos=(self.pos[0] + self.velo[0], self.pos[1] + self.velo[1])
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
        #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        #self.rotation=maths.degrees(maths.atan2(self.velo[1], self.velo[0]))+90 if self.velo[0] != 0 else 0
        if self.velo[1] > 0:
            self.rotation+=180

        if self.internalTimer >= self.lifespan:
            self.fuckOff=True
            if player.rect.colliderect([self.rect[0]-3, self.rect[1]-3, self.rect[2]+6, self.rect[3]+6]):
                player.health-=self.damage
                player.playOnCorrectChannel("hit")
            for bull in playerBullets:
                if bull.rect.colliderect([self.rect[0]-3, self.rect[1]-3, self.rect[2]+6, self.rect[3]+6]):
                    bull.fuckOff=True
            
        if player.rect.colliderect(self.rect):
            self.fuckOff=True
            player.health-=self.damage
            player.playOnCorrectChannel("hit")
            for bull in playerBullets:
                if bull.rect.colliderect([self.rect[0]-3, self.rect[1]-3, self.rect[2]+6, self.rect[3]+6]):
                    bull.fuckOff=True
        
        self.updateSprite()
    
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))
