import pygame as pg
from imageImporter import images
import particle
import random as rand
import math as maths

class playerBullet:
    def __init__(self, pos, velo, rotation, damage, lifespan, fps, screen:pg.Surface):
        self.pos=pos
        self.internalTimer=0
        self.lifespan=lifespan
        self.velo=velo
        self.baseVelo=velo
        self.rotation=rotation
        self.fps=fps
        self.damage=damage
        self.sprites=images["Projectiles"]["PlayerBullet"]
        self.currSprite=self.sprites[0]
        self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.fuckOff=False
        self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        self.screen=screen
    
    def updateSprite(self):
        if self.internalTimer%10 == 0:
            self.currSprite = rand.choice(self.sprites)
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
            #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])


    
    def update(self, maelstroms, boss, particles): 

        self.velo=(self.baseVelo[0]*(120/self.fps), self.baseVelo[1]*(120/self.fps))
        self.internalTimer+=(1/self.fps)

        self.pos=(self.pos[0] + self.velo[0], self.pos[1] - self.velo[1])
        radRot=maths.radians(self.rotation)
        rotated_offset_x = -10 * maths.sin(radRot)
        rotated_offset_y = 10 * maths.cos(radRot)

        partVelo=(0, 0)
        particles.append(particle.particle((self.pos[0]+rotated_offset_x, self.pos[1]-rotated_offset_y), partVelo, False, (255, 0, 0), 0.1, True, 100, self.fps, self.screen))
        #partVelo=(0, 0)
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
        #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])

        if self.internalTimer >= self.lifespan:
            self.fuckOff=True
        for strom in maelstroms:
            if strom.rect.colliderect(self.rect):
                strom.health-=self.damage
                self.fuckOff=True
                

        if boss.rect.colliderect(self.rect):
            self.fuckOff=True
            boss.health-=self.damage
            boss.hitsSinceLastSpeak+=1
            boss.playOnCorrectChannel("hit")
        self.updateSprite()
    
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))

class bossBullet:
    def __init__(self, pos, velo, rotation, damage, lifespan, texture, scale, fps, screen:pg.Surface):
        self.pos=pos
        self.internalTimer=0
        self.lifespan=lifespan
        self.velo=velo
        self.baseVelo=velo
        self.damage=damage
        self.texture=texture
        self.scale=scale
        self.fps=fps
        self.rotation=rotation
        self.sprites=images["Projectiles"][self.texture]
        self.currSprite=self.sprites[0]
        self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
        self.fuckOff=False
        self.currSprite = pg.transform.scale(self.currSprite, (self.currSprite.get_size()[0]*self.scale, self.currSprite.get_size()[1]*self.scale))
        self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        
        self.screen=screen
    
    def updateSprite(self):
        if self.internalTimer%10 == 0:
            self.currSprite = rand.choice(self.sprites)
            if self.texture!="BossPellet":
                self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.scale(self.currSprite, (self.currSprite.get_size()[0]*self.scale, self.currSprite.get_size()[1]*self.scale))
            self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
            #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])


    
    def update(self, player, particles): 
        self.velo=(self.baseVelo[0]*(120/self.fps), self.baseVelo[1]*(120/self.fps))
        self.internalTimer+=(1/self.fps)
        self.pos=(self.pos[0] + self.velo[0], self.pos[1] - self.velo[1])
        radRot=maths.radians(self.rotation)
        rotated_offset_x = -10 * maths.sin(radRot)
        rotated_offset_y = 10 * maths.cos(radRot)

        partVelo=(0, 0)
        particles.append(particle.particle((self.pos[0]+rotated_offset_x, self.pos[1]-rotated_offset_y), partVelo, False, (0, 145, 255), 0.1, True, 200, self.fps, self.screen))
        #particles.append(particle.particle((self.pos[0]+rotated_offset_x/2, self.pos[1]-rotated_offset_y/2), partVelo, False, (0, 145, 255), 0.1, True, 200, self.fps, self.screen))
        #particles.append(particle.particle((self.pos[0]+rotated_offset_x, self.pos[1]+rotated_offset_x), partVelo, False, (0, 145, 255), 0.1, True, 200, self.fps, self.screen))
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
        #self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
        if self.internalTimer >= self.lifespan:
            self.fuckOff=True
        if player.rect.colliderect(self.rect):
            self.fuckOff=True
            player.health-=self.damage
            player.playOnCorrectChannel("hit")
        self.updateSprite()
    
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))




