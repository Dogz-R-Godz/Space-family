import pygame as pg
from pygame import mixer
from imageImporter import images
import math as maths
import random as rand
import player as pla
import bossMaelstrom
import bullet
import time
import bossMissile
import coin
import bossMinion
import voicelinesImporter

class boss:
    def __init__(self, pos, screen:pg.Surface, tier, fps):
        self.pos=pos
        self.startingPos=pos
        self.internalTimer=0
        self.timeUntilNextBoss=5
        self.timeSinceSpawnedIn=0
        self.bossTier=tier 
        self.fps=fps
        self.invincibilityTimer=0
        self.startNextBoss=False
        self.profanityVoicelines=True
        if self.bossTier == 4:
            self.invincibilityTimer=90
        self.screen=screen
        self.weaponNames=[
            "bullets", 
            "pellets", 
            "missiles", 
            "maelstroms",
            "minions"
        ]
        self.weaponStats=[
            {   "bullets": {"dmg": 1, "speed": 1, "attackSpeed": 100, "sprite": "BossBullet", "amount": 1, "spray": 0, "scale": 1}},

            {   "bullets": {"dmg": 1, "speed": 2, "attackSpeed": 100, "sprite": "BossBullet", "amount": 1, "spray": 0, "scale": 1}, 
                "pellets": {"dmg": 1, "speed": 1, "attackSpeed": 200, "sprite": "BossPellet", "amount": 5, "spray": 10, "scale": 2}},
            
            {   
                "bullets": {"dmg": 1, "speed": 2.5, "attackSpeed": 75, "sprite": "BossBullet", "amount": 1, "spray": 0, "scale": 1},
                "pellets": {"dmg": 2, "speed": 3, "attackSpeed": 250, "sprite": "BossPellet", "amount": 9, "spray": 14, "scale": 2},
                "missiles": {"dmg": 3, "speed": 1, "attackSpeed": 250, "sprite": "N/A", "amount": 1, "spray": 0, "scale": 1}},
            
            {   
                "bullets": {"dmg": 1, "speed": 2.5, "attackSpeed": 65, "sprite": "BossBullet", "amount": 1, "spray": 0, "scale": 1},
                "pellets": {"dmg": 2, "speed": 3, "attackSpeed": 125, "sprite": "BossPellet", "amount": 15, "spray": 16, "scale": 2},
                "missiles": {"dmg": 3, "speed": 2, "attackSpeed": 200, "sprite": "N/A", "amount": 2, "spray": 5, "scale": 1},
                "maelstroms": {"dmg": 1, "speed": 2, "attackSpeed": 200, "shotSpeed": 25, "sprite": "N/A", "amount": 2, "spray": 5, "scale": 1}},
            
            {
                "bullets": {"dmg": 1, "speed": 2.5, "attackSpeed": 300, "sprite": "BossBullet", "amount": 1, "spray": 0, "scale": 1},
                "pellets": {"dmg": 2, "speed": 3, "attackSpeed": 600, "sprite": "BossPellet", "amount": 15, "spray": 16, "scale": 2},
                "missiles": {"dmg": 3, "speed": 3, "attackSpeed": 600, "sprite": "N/A", "amount": 2, "spray": 5, "scale": 1},
                "maelstroms": {"dmg": 1, "speed": 2, "attackSpeed": 600, "shotSpeed": 50, "sprite": "N/A", "amount": 2, "spray": 5, "scale": 1},
                "minions": {"dmg": 1, "speed": 0, "attackSpeed": 600, "shotSpeed": 240, "accuracy": 10}
            }
        ]
        self.bossStats=[
            {"health": 25, "maxHealth": 25, "speed": 1, "initCash": 300, "postCash": 40},
            {"health": 50, "maxHealth": 50, "speed": 2, "initCash": 400, "postCash": 50},
            {"health": 75, "maxHealth": 75, "speed": 2, "initCash": 600, "postCash": 60},
            {"health": 100, "maxHealth": 100, "speed": 3, "initCash": 800, "postCash": 80},
            {"health": 250, "maxHealth": 250, "speed": 4, "initCash": 1100, "postCash": 110},
        ]

        self.minionLookupBase=[
            (self.screen.get_width()-8, 8),
            (self.screen.get_width()-8, (self.screen.get_height()-80)//2),
            (self.screen.get_width()-8, (self.screen.get_height()-80)-8),
            (self.screen.get_width()//2, (self.screen.get_height()-80)-8),
            (8, (self.screen.get_height()-80)-8),
            (8, (self.screen.get_height()-80)//2),
            (8, 8), 
            (self.screen.get_width()//2, 8),

        ]
        self.minionLookupCopy=self.minionLookupBase.copy()


        #1: just bullets being fired. Actively avoids the player
        #2: bullets get faster and are shot faster. Slightly avoid player bullets. 
        #3: adds seeking missiles into the mix. Avoid player bullets more effectively. Position above player when shooting maelstrom. Maelstroms are shot in the direction of the player
        #4: adds minibosses that spawn in every now and then. Adds maelstroms into the mix.
        #5: ai neural network controls movement and learns as it goes

        self.audio={
            "theme1": mixer.Sound("Assets/Audio/backgroundMusic1.ogg"),
            "theme2": mixer.Sound("Assets/Audio/backgroundMusic2.ogg"),
            "theme3": mixer.Sound("Assets/Audio/backgroundMusic3.ogg"),
            "theme4": mixer.Sound("Assets/Audio/backgroundMusic4.ogg"),
            "moving": mixer.Sound("Assets/Audio/BossMoving.wav"),
            "hit": mixer.Sound("Assets/Audio/BossHit.wav"),
            "death": mixer.Sound("Assets/Audio/BossDeath.wav")
        }
        self.voicelines=voicelinesImporter.voiceLines[f"t{self.bossTier+1}"]
        self.audioChannels=[mixer.Channel(i+1) for i in range(7)]
        currTime=time.perf_counter()
        self.themeUpTo=1
        self.channelsTimeBeenPlaying=[currTime]*57
        #2: boss death, 3: boss hit, 4: boss hit, 5: boss hit, 6: boss moving, 7: music, 8: voicelines, 

        self.movementMode=0 #0: spinny, 1: follow above player, 2: go to random spot
        self.timeUntilNextMovement=0.01
        self.currMovementTime=0
        self.nextMove=-1
        self.velo=(0, 0)
        self.movementGoal=pos

        self.health=self.bossStats[self.bossTier]["health"]
        self.hitsSinceLastSpeak=0
        self.maxHealth=self.bossStats[self.bossTier]["maxHealth"]
        self.currShotCooldown=[50, 50, 50, 50, 120]
        
        self.speed=self.bossStats[self.bossTier]["speed"]

        self.sprites=images["Boss"] #"Boss"
        self.damageMask=self.sprites["muchDamage"][0]
        self.damageStatusSprites=self.sprites["noDamage"]

        # Create a copy of the original image to avoid modifying it directly
        
        #self.currSprite=self.damageStatusSprites[0]
        self.currSprite = self.damageStatusSprites[self.bossTier].copy()

        # Apply the mask
        self.currSprite.blit(self.damageMask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.currSprite.set_colorkey(self.currSprite.get_at((5, 0))[:3])
        self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
    
    def checkChannelsBusy(self):
        for channel in range(len(self.audioChannels)):
            if not self.audioChannels[channel].get_busy():
                self.channelsTimeBeenPlaying[channel]=time.perf_counter()
        
    def playOnCorrectChannel(self, sound):
        if sound == "death":
            if not self.audioChannels[0].get_busy():
                self.audioChannels[0].play(self.audio[sound])
                self.channelsTimeBeenPlaying[0]=time.perf_counter()
                self.audioChannels[0].set_volume(0.2)
        
        if sound == "hit":
            currTime=time.perf_counter()
            channelToPlayOn=self.channelsTimeBeenPlaying[1:4].index(min(self.channelsTimeBeenPlaying[1:4]))
            self.audioChannels[channelToPlayOn+1].stop()
            self.audioChannels[channelToPlayOn+1].play(self.audio[sound])
            self.audioChannels[channelToPlayOn+1].set_volume(0.2)
            self.channelsTimeBeenPlaying[channelToPlayOn+1]=currTime

        if sound == "moving":
            if not self.audioChannels[4].get_busy():
                self.audioChannels[4].play(self.audio[sound])
                self.channelsTimeBeenPlaying[4]=time.perf_counter()
                self.audioChannels[4].set_volume(0.2)
    def updateSprite(self):

        self.currSprite = self.damageStatusSprites[self.bossTier].copy()

        # Apply the mask
        if self.health < self.maxHealth//2:
            self.currSprite.blit(self.damageMask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        #self.currSprite = self.damageStatusSprites[0]
        self.currSprite.set_colorkey(self.currSprite.get_at((5, 0))[:3])
        self.rect = pg.Rect((self.currSprite.get_rect()[0]+self.pos[0]-self.currSprite.get_rect()[2]/2)-1, (self.currSprite.get_rect()[1]+self.pos[1]-self.currSprite.get_rect()[3]/2)-1, self.currSprite.get_rect()[2]+2, self.currSprite.get_rect()[3]+2)
    
    def update(self, bossMaelstroms, playerBullets, bossBullets, bossMissiles, bossMinions, coins, player: pla.player):
        self.voicelines=voicelinesImporter.voiceLines[f"t{self.bossTier+1}"]

        if not self.audioChannels[5].get_busy():
            self.audioChannels[5].play(self.audio[f"theme{self.themeUpTo}"])
            self.audioChannels[5].set_volume(0.1)
            self.themeUpTo+=1
            if self.themeUpTo == 5:
                self.themeUpTo == 1

        speedMultiplier=120/self.fps
        if self.bossTier==4 and self.invincibilityTimer > 0:
            self.currShotCooldown[4]-=speedMultiplier
        else:
            self.currShotCooldown[0]-=speedMultiplier
            self.currShotCooldown[1]-=speedMultiplier
            self.currShotCooldown[2]-=speedMultiplier
            self.currShotCooldown[3]-=speedMultiplier
        
        if self.timeSinceSpawnedIn == 0:
            if self.profanityVoicelines:
                self.audioChannels[6].stop()
                self.audioChannels[6].play(self.voicelines["start"])

        if self.hitsSinceLastSpeak >= max(self.maxHealth/5, 10):
            if self.profanityVoicelines:
                self.audioChannels[6].stop()
                self.audioChannels[6].play(rand.choice(self.voicelines["hit"]))
            self.hitsSinceLastSpeak=0

        self.internalTimer+=1
        self.timeSinceSpawnedIn+=1
        if self.health > 0:
            self.startNextBoss=False
            if self.invincibilityTimer>0:
                self.health = self.maxHealth
                self.invincibilityTimer-=(1/self.fps)
            else:
                if len(bossMinions) > 0:
                    if not bossMinions[0].fuckOff:
                        for minion in bossMinions:
                            minion.die()
                    if self.profanityVoicelines:
                        self.audioChannels[6].stop()
                        self.audioChannels[6].play(self.voicelines["start2"])
            self.timeUntilNextMovement+=1/self.fps
            if self.internalTimer % 5 == 0:
                self.checkChannelsBusy()    

            for weaponCount in range(self.bossTier+1):

                if self.currShotCooldown[weaponCount] <= 0:
                    if rand.randint(0, 4) == 0:
                        self.currShotCooldown[weaponCount]=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["attackSpeed"]

                        if weaponCount == 0 or weaponCount == 1:
                            playerDistance=maths.sqrt((self.pos[0]-player.pos[0])**2 + (self.pos[1]-player.pos[1])**2)
                            multiplier=1/playerDistance
                            multiplier*=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]
                            amountOfProj=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["amount"]
                            amountOnEachSide=(amountOfProj-1)/2
                            rotationMul=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["spray"]/amountOnEachSide if amountOnEachSide != 0 else 0
                            rotation=maths.degrees(maths.atan2((self.pos[1]-player.pos[1]), (self.pos[0]-player.pos[0])))+90 if (self.pos[0]-player.pos[0]) != 0 else 0
                            rotation=0-rotation
                            #rotation+=90
                            #if (player.pos[1]-self.pos[1]) < 0:
                                #rotation=maths.degrees(maths.atan2(-(self.pos[0]-player.pos[0])/-(self.pos[1]-player.pos[1]))) if (self.pos[0]-player.pos[0]) != 0 else 0
                            xAdder1=maths.sin(maths.radians(rotation+180))
                            yAdder1=maths.cos(maths.radians(rotation+180))
                            
                            for x in range(int(amountOnEachSide)):
                                newRot=rotationMul*(x+1)
                                newRot+=rotation
                                newRot2=-rotationMul*(x+1)
                                newRot2+=rotation
                                xAdder=maths.sin(maths.radians(newRot+180))
                                yAdder=maths.cos(maths.radians(newRot+180))
                                xAdder2=maths.sin(maths.radians(newRot2+180))
                                yAdder2=maths.cos(maths.radians(newRot2+180))
                                #bossBullets.append(bullet.bossBullet(self.pos, ((xAdder*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]), (-(player.pos[1]-self.pos[1])*multiplier)+yAdder), newRot, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 810, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["sprite"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["scale"], self.screen))
                                #bossBullets.append(bullet.bossBullet(self.pos, (((player.pos[0]-self.pos[0])*multiplier)-xAdder, (-(player.pos[1]-self.pos[1])*multiplier)+yAdder), newRot, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 810, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["sprite"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["scale"], self.screen))
                                bossBullets.append(bullet.bossBullet(self.pos, ((-xAdder*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]), (yAdder*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"])), newRot, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 6.75, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["sprite"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["scale"], self.fps, self.screen))
                                bossBullets.append(bullet.bossBullet(self.pos, ((-xAdder2*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]), (yAdder2*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"])), newRot, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 6.75, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["sprite"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["scale"], self.fps, self.screen))
                            bossBullets.append(bullet.bossBullet(self.pos, ((-xAdder1*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]), (yAdder1*self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"])), rotation, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 6.75, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["sprite"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["scale"], self.fps, self.screen))
                        
                        if weaponCount == 2:
                            playerDistance=maths.sqrt((self.pos[0]-player.pos[0])**2 + (self.pos[1]-player.pos[1])**2)
                            multiplier=1/playerDistance
                            multiplier*=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]

                            amountOfProj=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["amount"]
                            amountOnEachSide=(amountOfProj-1)/2
                            rotationMul=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["spray"]/amountOnEachSide if amountOnEachSide != 0 else 0
                            rotation=maths.degrees(maths.tanh((self.pos[1]-player.pos[1])/(self.pos[0]-player.pos[0]))) if (self.pos[0]-player.pos[0]) != 0 else 0
                            if (player.pos[1]-self.pos[1]) < 0:
                                rotation+=180
                            
                            for x in range(int(amountOnEachSide)):
                                newRot=rotationMul*(x+1)
                                newRot+=rotation
                                bossMissiles.append(bossMissile.bossMissile(self.pos, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], newRot, 6.75, self.screen))

                            bossMissiles.append(bossMissile.bossMissile(self.pos, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], rotation, 6.75, self.fps, self.screen))
                            x=0
                        
                        if weaponCount == 3:
                            
                            playerDistance=maths.sqrt((self.pos[0]-player.pos[0])**2 + (self.pos[1]-player.pos[1])**2)
                            multiplier=1/playerDistance
                            multiplier*=self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["speed"]
                            bossMaelstroms.append(bossMaelstrom.bossMaelstrom(self.pos, ((player.pos[0]-self.pos[0])*multiplier, -(player.pos[1]-self.pos[1])*multiplier), 4, 6.75, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["shotSpeed"], 2, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 5, 8, self.fps, self.screen))
                        
                        if weaponCount == 4:
                            if len(self.minionLookupCopy) != 0:
                                pos=rand.choice(self.minionLookupCopy)
                                self.minionLookupCopy.pop(self.minionLookupCopy.index(pos))
                                bossMinions.append(bossMinion.bossMinion(self.pos, pos, self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["shotSpeed"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["accuracy"], self.weaponStats[self.bossTier][self.weaponNames[weaponCount]]["dmg"], 10, 2, self.fps, self.screen))
                        

                        # if player.pos[1] < self.pos[1]:
                        #     bossMaelstroms.append(bossMaelstrom.bossMaelstrom(self.pos, (0, 2), 3, 400, self.stromShotCooldown, self.bulletDamage, 120, 8, self.screen))
                        # else:
                        #     bossMaelstroms.append(bossMaelstrom.bossMaelstrom(self.pos, (0, -2), 3, 400, self.stromShotCooldown, self.bulletDamage, 120, 8, self.screen))

            if self.timeUntilNextMovement >= self.currMovementTime: #0: spinny, 1: follow above player, 2: go to random spot
                if self.movementMode == 0:
                    self.pos = self.movementGoal
                if self.nextMove == -1:
                    self.movementMode = rand.randint(0, 2) if self.bossTier <= 1 else rand.randint(1, 3)
                else:
                    self.movementMode = self.nextMove
                self.currMovementTime = rand.randint(round(2), round(5)) #between 2 seconds and 6 seconds
                self.timeUntilNextMovement = 0.01
                self.playOnCorrectChannel("moving")
                if self.movementMode == 2:
                    self.movementGoal = (rand.randint(50, 490), rand.randint(50, 760))
                    self.velo=((self.movementGoal[0]-self.pos[0])/(self.currMovementTime/self.speed), (self.movementGoal[1]-self.pos[1])/(self.currMovementTime/self.speed))
                elif self.movementMode == 0:
                    self.movementGoal=self.pos
                    self.velo=(0, 0)
                elif self.movementMode == 3:
                    self.nextMove==4
                    self.movementMode=2
                    spinSpot=player.pos
                    angle=rand.randint(0, 360)
                    self.movementGoal = ((200*maths.sin(angle/(speedMultiplier*5))) + spinSpot[0], (200*maths.cos(angle/(speedMultiplier*5))) + spinSpot[1])
                    self.velo=((self.movementGoal[0]-self.pos[0])/(self.currMovementTime/self.speed), (self.movementGoal[1]-self.pos[1])/(self.currMovementTime/self.speed))
                    self.nextMove=-1
            
            
            # if self.bossTier == 0:
            #     if maths.sqrt((self.pos[0]-player.pos[0])**2 + (self.pos[1]-player.pos[1])**2) < 100:
            #         distanceX=(self.pos[0]-player.pos[0])
            #         distanceY=(self.pos[1]-player.pos[1])
            #         distanceSum=distanceX+distanceY
            #         self.velo = (((distanceX/distanceSum)*speedMultiplier)+self.velo[0], ((distanceX/distanceSum)*speedMultiplier)+self.velo[1])
            #         #self.movementGoal = (((self.pos[0]-player.pos[0])/50)+self.movementGoal[0], ((self.pos[1]-player.pos[1])/50)+self.movementGoal[1])
            #         #self.movementGoal = (max(min(self.movementGoal[0], 540), 0), max(min(self.movementGoal[1], 810), 0))

            
             #0: spinny, 1: follow above player, 2: go to random spot
            if self.movementMode == 0:
                #self.movementGoal = (max(min(self.movementGoal[0]+self.velo[0], 490), 50), max(min(self.movementGoal[1]-self.velo[1], 760), 50))
                spinSpot=self.movementGoal
                newPos=((20*maths.sin(maths.radians((self.timeUntilNextMovement)))) + spinSpot[0], (20*maths.cos(maths.radians(self.timeUntilNextMovement))) + spinSpot[1])
                self.velo=(newPos[0]-self.pos[0])
                self.pos=newPos
                self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
            if self.movementMode == 1:
                self.movementGoal = (player.pos[0], max(player.pos[1]-490, 50))
                self.velo=((self.movementGoal[0]-self.pos[0])/((self.currMovementTime*self.speed))*3, ((self.movementGoal[1]-self.pos[1])/(self.currMovementTime*self.speed))*3)
                self.pos = (max(min(self.pos[0]+(self.velo[0]/self.fps), 490), 50), max(min(self.pos[1]+(self.velo[1]/self.fps), 760), 50))
                self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
            if self.movementMode == 2:
                self.pos = (max(min(self.pos[0]+(self.velo[0]/self.fps), 490), 50), max(min(self.pos[1]+(self.velo[1]/self.fps), 760), 50))
                self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
            if self.movementMode == 4:
                spinSpot=player.pos
                newPos=((200*maths.sin(self.timeUntilNextMovement)) + spinSpot[0], (200*maths.cos(self.timeUntilNextMovement)) + spinSpot[1])
                self.velo=(newPos[0]-self.pos[0])
                self.pos=newPos
                self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])
            self.updateSprite()

        else:
            if self.timeUntilNextBoss == 5:
                
                if player.bossTiersBeaten[self.bossTier]:
                    for x in range(5):
                        coins.append(coin.coin((self.pos[0]+rand.randint(-10, 10), self.pos[0]+rand.randint(-10, 10)), self.bossStats[self.bossTier]["postCash"]/5, self.screen))
                else:
                    for x in range(5):
                        coins.append(coin.coin((self.pos[0]+rand.randint(-10, 10), self.pos[0]+rand.randint(-10, 10)), self.bossStats[self.bossTier]["initCash"]/5, self.screen))
                self.pos=(-500, -500)
                player.bossTiersBeaten[self.bossTier] = True
                self.timeUntilNextBoss-=1/self.fps
                if self.profanityVoicelines:
                    self.audioChannels[6].stop()
                    self.audioChannels[6].play(self.voicelines["death"])
            if self.startNextBoss:
                self.timeUntilNextBoss-=1/self.fps
            if self.timeUntilNextBoss <= 0:
                self.timeSinceSpawnedIn=0
                self.startNextBoss=False
                self.timeUntilNextBoss=5
                self.playOnCorrectChannel("death")
                self.hitsSinceLastSpeak=0

                
                
                player.pos=player.startingPos
                player.health=player.fullHealth
                
                self.bossTier+=1
                if self.bossTier == 4:
                    self.invincibilityTimer=90

                for mael in bossMaelstroms:
                    mael.fuckOff=True
                for bull in playerBullets:
                    bull.fuckOff=True
                for bull in bossBullets:
                    bull.fuckOff=True
                for miss in bossMissiles:
                    miss.fuckOff=True

                self.pos=self.startingPos
                self.movementMode=0 #0: spinny, 1: follow above player, 2: go to random spot
                self.timeUntilNextMovement=0
                self.velo=(0, 0)
                self.movementGoal=self.startingPos

                self.health=self.bossStats[self.bossTier]["health"]
                self.maxHealth=self.bossStats[self.bossTier]["maxHealth"]
                self.currShotCooldown=[50, 50, 50, 50, 120]
                self.speed=self.bossStats[self.bossTier]["speed"]

                self.sprites=images["Boss"] #"Boss"
                if self.health < self.maxHealth/2:
                    self.damageStatusSprites=self.sprites["muchDamage"]
                else:
                    self.damageStatusSprites=self.sprites["noDamage"]
                self.currSprite=self.damageStatusSprites[0]
                self.currSprite.set_colorkey(self.currSprite.get_at((5, 0))[:3])
                self.rect = pg.Rect(self.currSprite.get_rect()[0]+self.pos[0], self.currSprite.get_rect()[1]+self.pos[1], self.currSprite.get_rect()[2], self.currSprite.get_rect()[3])

    def render(self):
        self.screen.blit(self.currSprite, (self.pos[0] - (self.currSprite.get_width()/2), self.pos[1] - (self.currSprite.get_height()/2)))

        
