import pygame as pg
import pygame.mixer as mixer
from imageImporter import images
import math as maths
import random as rand
import bullet
import time
import particle

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

class player:
    def __init__(self, pos, velo, rotation, health, damage, shotCooldown, initShotCooldown, screen:pg.Surface, controlMethod:int, upgrades, fps, cash, shootAtMouse):
        self.pos=pos
        self.startingPos=pos
        self.internalTimer=0
        self.bulletsShot=0
        self.velo=velo
        self.rotVelo=0
        self.rotation=rotation
        self.rotationChange=0
        self.health=health
        self.fps=fps
        self.cash=cash
        self.upgrades=upgrades
        self.bossTiersBeaten=[False, False, False, False, False]
        self.shootAtMouse=shootAtMouse
        speedMultiplier=120/self.fps

        self.audio={
            "moving": mixer.Sound("Assets/Audio/PlayerMoving.wav"),
            "hit": mixer.Sound("Assets/Audio/PlayerHit.wav"),
            "firing": mixer.Sound("Assets/Audio/PlayerFiring.wav")
        }
        self.audioChannels=[mixer.Channel(i+8) for i in range(57)]
        currTime=time.time()
        self.channelsTimeBeenPlaying=[currTime]*57
        for channel in self.audioChannels:
            channel.stop()
        #7: player firing, 8: player firing, 9: player hit, 10: player hit, 11: player hit, 12: player moving

        self.sprites=images["Player"]
        if self.health < 5:
            self.damageStatusSprites=self.sprites["muchDamage"]
        else:
            self.damageStatusSprites=self.sprites["noDamage"]
        self.currSprite=self.damageStatusSprites["Idle"][0]
        self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0]-2, self.currSprite.get_rect()[1]+self.pos[1]-2, self.currSprite.get_rect()[2]-4, self.currSprite.get_rect()[3]-4)

        self.damage=self.upgrades["Weapon"]["upgrades"]["Damage"]["level"]+1
        self.speed=(self.upgrades["Player"]["upgrades"]["Speed"]["level"]*0.5)+2
        self.shotCooldown=0.25-(self.upgrades["Weapon"]["upgrades"]["AttackSpeed"]["level"]*0.05)
        self.fullHealth=(self.upgrades["Player"]["upgrades"]["Health"]["level"]+1)*20
        self.currShotCooldown=initShotCooldown
        self.screen=screen
        self.controlMethod=controlMethod
    
    def checkChannelsBusy(self):
        for channel in range(len(self.audioChannels)):
            if not self.audioChannels[channel].get_busy():
                self.channelsTimeBeenPlaying[channel]=time.time()
    
    def playOnCorrectChannel(self, sound):
        if sound == "firing":
            channelToPlayOn=self.channelsTimeBeenPlaying[0:2].index(min(self.channelsTimeBeenPlaying[0:2]))
            self.audioChannels[channelToPlayOn].stop()
            self.audioChannels[channelToPlayOn].play(self.audio[sound])
            self.audioChannels[channelToPlayOn].set_volume(0.2)
            self.channelsTimeBeenPlaying[channelToPlayOn]=time.time()
        
        if sound == "hit":
            channelToPlayOn=self.channelsTimeBeenPlaying[2:56].index(min(self.channelsTimeBeenPlaying[2:56]))
            self.audioChannels[channelToPlayOn+2].stop()
            self.audioChannels[channelToPlayOn+2].play(self.audio[sound])
            self.audioChannels[channelToPlayOn+2].set_volume(0.2)
            self.channelsTimeBeenPlaying[channelToPlayOn]=time.time()

        if sound == "moving":
            if not self.audioChannels[56].get_busy():
                self.audioChannels[56].play(self.audio[sound])
                self.channelsTimeBeenPlaying[56]=time.time()
                self.audioChannels[56].set_volume(0.2)
    def setCurrSprite(self):
        speedMultiplier=120/self.fps
        if self.health < 5:
            self.damageStatusSprites=self.sprites["muchDamage"]
        else:
            self.damageStatusSprites=self.sprites["noDamage"]
        if self.velo == (0, 0):
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Idle"][0], (self.damageStatusSprites["Idle"][0].get_size()[0]*2, self.damageStatusSprites["Idle"][0].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[0]) <= (self.speed/3)*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][0], (self.damageStatusSprites["Accelerating"][0].get_size()[0]*2, self.damageStatusSprites["Accelerating"][0].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[1]) <= (self.speed/3)*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][0], (self.damageStatusSprites["Accelerating"][0].get_size()[0]*2, self.damageStatusSprites["Accelerating"][0].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[1])+abs(self.velo[0]) <= (self.speed/2)*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][0], (self.damageStatusSprites["Accelerating"][0].get_size()[0]*2, self.damageStatusSprites["Accelerating"][0].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[0]) > (self.speed/3)*speedMultiplier and abs(self.velo[0]) <= (self.speed/3)*2*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][1], (self.damageStatusSprites["Accelerating"][1].get_size()[0]*2, self.damageStatusSprites["Accelerating"][1].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[1]) > (self.speed/3)*speedMultiplier and abs(self.velo[1]) <= (self.speed/3)*2*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][1], (self.damageStatusSprites["Accelerating"][1].get_size()[0]*2, self.damageStatusSprites["Accelerating"][1].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[1])+abs(self.velo[0]) > (self.speed/2)*speedMultiplier and abs(self.velo[1])+abs(self.velo[0]) <= self.speed*speedMultiplier:
            self.currSprite = pg.transform.scale(self.damageStatusSprites["Accelerating"][1], (self.damageStatusSprites["Accelerating"][1].get_size()[0]*2, self.damageStatusSprites["Accelerating"][1].get_size()[1]*2))
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
        if abs(self.velo[0]) > (self.speed/3)*2*speedMultiplier or abs(self.velo[1]) > (self.speed/3)*2*speedMultiplier or abs(self.velo[1])+abs(self.velo[0]) > self.speed*speedMultiplier:
            self.currSprite = rand.choice(self.damageStatusSprites["Moving"])
            self.currSprite = pg.transform.scale(self.currSprite, (self.currSprite.get_size()[0]*2, self.currSprite.get_size()[1]*2))
            self.currSprite = pg.transform.rotate(self.currSprite, self.rotation)
            self.currSprite.set_colorkey(self.currSprite.get_at((0, 0))[:3])
            
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1*(self.upgrades["Player"]["upgrades"]["SmallerHitbox"]["level"]+1), (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1*(self.upgrades["Player"]["upgrades"]["SmallerHitbox"]["level"]+1), self.currSprite.get_rect()[2]-2*(self.upgrades["Player"]["upgrades"]["SmallerHitbox"]["level"]+1), self.currSprite.get_rect()[3]-2*(self.upgrades["Player"]["upgrades"]["SmallerHitbox"]["level"]+1))

    def update(self, keysDown, bullets, particles):
        #keysDown: right, left, up, down, shoot
        self.currShotCooldown+=1/self.fps
        self.internalTimer+=1
        if self.internalTimer % 5 == 0:
            self.checkChannelsBusy()
        speedMultiplier=120/self.fps
        self.damage=self.upgrades["Weapon"]["upgrades"]["Damage"]["level"]+1
        self.speed=(self.upgrades["Player"]["upgrades"]["Speed"]["level"]*0.5)+1
        self.shotCooldown=0.25-(self.upgrades["Weapon"]["upgrades"]["AttackSpeed"]["level"]*0.05)
        self.fullHealth=(self.upgrades["Player"]["upgrades"]["Health"]["level"]+1)*20
        

        if self.controlMethod == 0:
            if keysDown[0]:
                self.velo = (min(self.velo[0]+0.05/speedMultiplier, self.speed), self.velo[1])
            if keysDown[1]:
                self.velo = (max(self.velo[0]-0.05/speedMultiplier, -self.speed), self.velo[1])
            if not (keysDown[0] ^ keysDown[1]):
                if self.velo[0] > 0:
                    self.velo = (max(self.velo[0]-0.025/speedMultiplier, 0), self.velo[1])
                else:
                    self.velo = (min(self.velo[0]+0.025/speedMultiplier, 0), self.velo[1])
            if keysDown[2]:
                self.velo = (self.velo[0], max(self.velo[1]-0.05/speedMultiplier, -self.speed))
            if keysDown[3]:
                self.velo = (self.velo[0], min(self.velo[1]+0.05/speedMultiplier, self.speed))
            if not (keysDown[2] ^ keysDown[3]):
                if self.velo[1] > 0:
                    self.velo = (self.velo[0], max(self.velo[1]-0.025/speedMultiplier, 0))
                else:
                    self.velo = (self.velo[0], min(self.velo[1]+0.025/speedMultiplier, 0))
            if keysDown[4]:
                
                if self.currShotCooldown <= 0:
                    self.currShotCooldown=self.shotCooldown
                    xAdder=maths.sin(maths.radians(self.rotation+180))
                    yAdder=maths.cos(maths.radians(self.rotation+180))

                    xAdder2=maths.sin(maths.radians(self.rotation+90))
                    yAdder2=maths.cos(maths.radians(self.rotation+90))
                    self.bulletsShot+=1
                    if self.bulletsShot % 2 == 0:
                        bullets.append(bullet.playerBullet((self.pos[0]-(xAdder2*10), self.pos[1]-(yAdder2*10)), (xAdder*10*speedMultiplier, yAdder*-10*speedMultiplier), self.rotation, self.damage, 1000, self.screen))
                    else:
                        bullets.append(bullet.playerBullet((self.pos[0]+(xAdder2*10), self.pos[1]-(yAdder2*10)), (xAdder*10*speedMultiplier, yAdder*-10*speedMultiplier), self.rotation, self.damage, 1000, self.screen))
            
            newRot=maths.degrees(maths.tanh(self.velo[1]/self.velo[0])) if self.velo[0] != 0 else 0
            if self.velo[1] > 0:
                newRot+=180

            if newRot != 0:
                self.rotation = newRot
            self.pos = (max(min(self.pos[0]+self.velo[0], 540), 0), max(min(self.pos[1]+self.velo[1], 810), 0))
            self.rect=pg.Rect(self.currSprite.get_rect()[0]+self.pos[0]-2, self.currSprite.get_rect()[1]+self.pos[1]-2, self.currSprite.get_rect()[2]-4, self.currSprite.get_rect()[3]-4)
            
        if self.controlMethod == 1:
            rotOld=self.rotation



            if keysDown[0]:
                self.rotation-=1.5*speedMultiplier
                
            if keysDown[1]:
                self.rotation+=1.5*speedMultiplier
            #self.rotVelo=max(min(self.rotVelo, self.speed/2), -self.speed/2)
            #self.rotation+=self.rotVelo
            self.rotation %= 360
            self.rotationChange = rotOld-self.rotation
            xAdder=maths.sin(maths.radians(self.rotation+180))*(self.speed/1.25)*speedMultiplier
            yAdder=maths.cos(maths.radians(self.rotation+180))*(self.speed/1.25)*speedMultiplier
            #adderSum=abs(xAdder)+abs(yAdder)
            #xAdder=xAdder/adderSum
            #yAdder=yAdder/adderSum
            
            if keysDown[2]:
                decay_factor = (1 / 1.15) ** (speedMultiplier * 120)
                self.velo=(max(min((self.velo[0]*decay_factor)+xAdder, self.speed*speedMultiplier), -self.speed*speedMultiplier), max(min((self.velo[1]*decay_factor)+yAdder, self.speed*speedMultiplier), -self.speed*speedMultiplier))
                
                rotated_offset_x = 15 * maths.cos(maths.radians(self.rotation+90)) - 7 * maths.sin(maths.radians(self.rotation+90))
                rotated_offset_y = 15 * maths.sin(maths.radians(self.rotation+90)) + 7 * maths.cos(maths.radians(self.rotation+90))
                

                # Calculate the second position
                partVelo=(-self.velo[0]/3, -self.velo[1]/3)
                particles.append(particle.particle((self.pos[0]-rotated_offset_x, self.pos[1]+rotated_offset_y), partVelo, False, (70, 246, 255), 0.2, True, 200, self.fps, self.screen))

                rotated_offset_x = 15 * maths.cos(maths.radians(self.rotation+90)) + 7 * maths.sin(maths.radians(self.rotation+90))
                rotated_offset_y = 15 * maths.sin(maths.radians(self.rotation+90)) - 7 * maths.cos(maths.radians(self.rotation+90))
                particles.append(particle.particle((self.pos[0]-rotated_offset_x, self.pos[1]+rotated_offset_y), partVelo, False, (70, 246, 255), 0.2, True, 200, self.fps, self.screen))
                #pg.draw.circle(self.screen, (255, 0, 0), (self.pos[0]-rotated_offset_x, self.pos[1]+rotated_offset_y), 3)
                #pg.draw.circle(self.screen, (255, 0, 0), (self.pos[0]+rotated_offset_x, self.pos[1]+rotated_offset_y), 3)

                self.playOnCorrectChannel("moving")
            else:
                
                if self.velo[1] > 0:
                    self.velo = (self.velo[0], max(self.velo[1]-0.01*speedMultiplier, 0))
                else:
                    self.velo = (self.velo[0], min(self.velo[1]+0.01*speedMultiplier, 0))

                if self.velo[0] > 0:
                    self.velo = (max(self.velo[0]-0.01*speedMultiplier, 0), self.velo[1])
                else:
                    self.velo = (min(self.velo[0]+0.01*speedMultiplier, 0), self.velo[1])
            if not keysDown[0] and not keysDown[1]:
                if self.rotVelo > 0:
                    self.rotVelo=max(self.rotVelo-0.15*speedMultiplier, 0)
                else:
                    self.rotVelo=min(self.rotVelo+0.15*speedMultiplier, 0)
            if keysDown[3]:
                brakes=(self.upgrades["Player"]["upgrades"]["Brakes"]["level"]+1)*0.05/speedMultiplier
                if self.velo[1] > 0:
                    self.velo = (self.velo[0], max(self.velo[1]-brakes*speedMultiplier, 0))
                else:
                    self.velo = (self.velo[0], min(self.velo[1]+brakes*speedMultiplier, 0))

                if self.velo[0] > 0:
                    self.velo = (max(self.velo[0]-brakes*speedMultiplier, 0), self.velo[1])
                else:
                    self.velo = (min(self.velo[0]+brakes*speedMultiplier, 0), self.velo[1])
                if self.rotVelo > 0:
                    self.rotVelo=max(self.rotVelo-0.25*speedMultiplier, 0)
                else:
                    self.rotVelo=min(self.rotVelo+0.25*speedMultiplier, 0)
            
            if keysDown[4]:
                if self.currShotCooldown >= self.shotCooldown:
                    self.currShotCooldown=0
                    
                    if self.upgrades["Weapon"]["upgrades"]["AimAtMouse"]["level"] == 0:
                        xAdder=maths.sin(maths.radians(self.rotation+180))
                        yAdder=maths.cos(maths.radians(self.rotation+180))
                        xAdder2=maths.sin(maths.radians(self.rotation+90))
                        yAdder2=maths.cos(maths.radians(self.rotation+90))
                        bulletSpeed=(self.upgrades["Weapon"]["upgrades"]["LaserSpeed"]["level"]+1)*5
                        self.bulletsShot+=1
                        if self.bulletsShot % 2 == 0:
                            bullets.append(bullet.playerBullet((self.pos[0]-(xAdder2*10), self.pos[1]-(yAdder2*10)), (xAdder*bulletSpeed, yAdder*-bulletSpeed), self.rotation, self.damage, 8, self.fps, self.screen))
                        else:
                            bullets.append(bullet.playerBullet((self.pos[0]+(xAdder2*10), self.pos[1]+(yAdder2*10)), (xAdder*bulletSpeed, yAdder*-bulletSpeed), self.rotation, self.damage, 8, self.fps, self.screen))
                        self.playOnCorrectChannel("firing")
                    else:
                        # mousePos=pg.mouse.get_pos()
                        # diffX=mousePos[0]-self.pos[0]
                        # diffY=mousePos[1]-self.pos[1]
                        # angle=maths.degrees(maths.atan(diffX/diffY)) if diffY != 0 else 0
                        # if diffY>=0:angle+=180
                        # if angle-self.rotation > 15:
                        #     angle=self.rotation+15
                        # if angle-self.rotation < -15:
                        #     angle=self.rotation-15

                        mousePos = pg.mouse.get_pos()
                        bulletSpeed=(self.upgrades["Weapon"]["upgrades"]["LaserSpeed"]["level"]+1)*5
                        diffX = mousePos[0] - self.pos[0]
                        diffY = mousePos[1] - self.pos[1]

                        # Use atan2 instead of atan - handles all quadrants correctly
                        target_angle = maths.degrees(maths.atan2(-diffY, diffX))+90  # Negative diffY because pygame Y is inverted

                        # Normalize angles to 0-360
                        target_angle = target_angle % 360
                        current_rotation = self.rotation % 360

                        # Calculate the smallest angle difference
                        angle_diff = ((target_angle - current_rotation) % 360) - 180

                        # Apply the rotation rules
                        
                        angleAllowed={1: 15, 2: 30, 3: 45}[self.upgrades["Weapon"]["upgrades"]["AimAtMouse"]["level"]]

                        if abs(angle_diff) <= angleAllowed:
                            # Within 15 degrees - use target angle
                            angle = (target_angle+180) % 360
                        elif abs(angle_diff) <= 90:
                            # Between 15 and 90 degrees - limit to ±15 degrees
                            if angle_diff > 0:
                                angle = current_rotation + angleAllowed
                            else:
                                angle = current_rotation - angleAllowed
                        else:
                            # More than 90 degrees - keep current rotation
                            angle = current_rotation
                        
                        xAdder2=maths.sin(maths.radians(self.rotation+90))
                        yAdder2=maths.cos(maths.radians(self.rotation+90))
                        xAdder=maths.sin(maths.radians(angle+180))
                        yAdder=maths.cos(maths.radians(angle+180))
                        self.bulletsShot+=1
                        if self.bulletsShot % 2 == 0:
                            bullets.append(bullet.playerBullet((self.pos[0]-(xAdder2*12), self.pos[1]-(yAdder2*12)), (xAdder*bulletSpeed/speedMultiplier, yAdder*-bulletSpeed/speedMultiplier), angle, self.damage, 8, self.fps, self.screen))
                        else:
                            bullets.append(bullet.playerBullet((self.pos[0]+(xAdder2*12), self.pos[1]-(yAdder2*12)), (xAdder*bulletSpeed/speedMultiplier, yAdder*-bulletSpeed/speedMultiplier), angle, self.damage, 8, self.fps, self.screen))

            #elif keysDown[3]:s
                #self.velo=(clamp(self.velo[0]-maths.cos(maths.radians(self.rotation))*0.5, 0, ), -max(min(self.velo[1]-maths.sin(maths.radians(self.rotation))*0.5, 0), 0))
            
            
            self.pos = (max(min(self.pos[0]+self.velo[0], 510), 30), max(min(self.pos[1]+self.velo[1], 780), 30))
        self.setCurrSprite()
        
    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))
        #xAdder2=maths.sin(maths.radians(self.rotation+270))
        #yAdder2=maths.cos(maths.radians(self.rotation+270))
        
    