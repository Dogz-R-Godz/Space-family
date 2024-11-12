import pygame as pg
from imageImporter import images
import math as maths
from bullet import bossBullet

class bossMaelstrom:
    def __init__(self, pos, velo, health, lifespan, shotCooldown, initShotCooldown, bulletDamage, bulletLifespan, bulletCount, fps, screen:pg.Surface):
        self.pos=pos
        self.internalTimer=0
        self.fps=fps
        self.shotCooldown=shotCooldown
        self.currCooldown=initShotCooldown
        self.bulletDamage=bulletDamage
        self.bulletLifespan=bulletLifespan
        self.bulletCount=bulletCount
        self.lifespan=lifespan
        self.velo=velo
        self.health=health
        self.spriteNum=0
        self.sprites=images["Projectiles"]["BossMaelstrom"]
        self.currSprite=self.sprites[self.spriteNum]
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.fuckOff=False
        self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.screen=screen
    
    def updateSprite(self):
        if self.internalTimer%10 == 0:
            self.currSprite = self.sprites[self.spriteNum]
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2), (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2), self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])


    
    def update(self, bossBullets): 
        self.internalTimer+=(1/self.fps)
        self.currCooldown-=(1/self.fps)
        if self.internalTimer >= self.lifespan:
            self.fuckOff=True
        if self.health <= 0:
            self.fuckOff=True
        
        if self.currCooldown <= 0:
            self.currCooldown=self.shotCooldown

            multiplier=360/self.bulletCount

            for x in range(self.bulletCount):
                x2=x+(self.internalTimer/105)
                dirX = maths.sin(maths.radians(x2*multiplier))
                dirY = maths.cos(maths.radians(x2*multiplier))
                bossBullets.append(bossBullet(self.pos, (dirX*2, dirY*2), 0, self.bulletDamage, self.bulletLifespan, "BossPellet", 1, self.fps, self.screen))
        self.pos=(self.pos[0] + self.velo[0], self.pos[1] - self.velo[1])
        self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.updateSprite()
    
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))