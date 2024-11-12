import pygame as pg
from pygame import mixer
import pickle as pkl
import random as rand
import math as maths



pg.init()
mixer.init() 
mixer.set_num_channels(66)
audio=mixer.Sound("Assets/Audio/ButtonClick.wav")
channel=mixer.Channel(0)
#0: background music, 1: button clicks, 
#2: boss death, 3: boss hit, 4: boss hit, 5: boss hit, 6: boss moving, 
#7: player firing, 8: player firing, 9-62: player hit, 12: player moving



BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (80, 80, 80)
DARK_GREY = (60, 60, 60)
DARKER_GREY = (40, 40, 40)
size = (540, 900)

vsync=1

screen = pg.display.set_mode(size, flags=pg.SCALED, vsync=vsync)

#screen = pg.display.set_mode(size, flags=pg.SCALED, vsync=vsync)

font = pg.font.Font('FreeSansBold.ttf', 32)

smallFont = pg.font.Font('FreeSansBold.ttf', 16)

costFont = pg.font.Font('FreeSansBold.ttf', 10)

cashFont = pg.font.Font('FreeSansBold.ttf', 24)

import imageImporter
import voicelinesImporter

fps=120
profanityVoicelines=0

screen.fill(DARKER_GREY)

titleFont = pg.font.Font('FreeSansBold.ttf', 50)
title = titleFont.render(f'SPACE FAMILY', False, WHITE, None)
titleRect = title.get_rect()
titleRect.center = (270, 100)


play = font.render(f'PLAY', False, WHITE, None)
playRect = play.get_rect()
playRect.center = (150, 300)


options = font.render(f'OPTIONS', False, WHITE, None)
optionsRect = options.get_rect()
optionsRect.center = (150, 400)


stop = font.render(f'QUIT', False, WHITE, None)
stopRect = stop.get_rect()
stopRect.center = (150, 500)

shop = cashFont.render('SHOP', False, WHITE, None)
shopRect = shop.get_rect()
shopRect.center = (50, 880)

shopIcon=imageImporter.images["Projectiles"]["CashPellet"][0]
shopIcon.set_colorkey(shopIcon.get_at((0, 0))[:3])
shopIcon = pg.transform.scale(shopIcon, (50, 50))
shopIconRect = shopIcon.get_rect()
shopIconRect.center = (50, 845)


stars=[
    pg.transform.scale(pg.image.load("Assets/Stars/Star1.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star2.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star3.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star4.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star3.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star2.png").convert_alpha(), (10, 10)),
    pg.transform.scale(pg.image.load("Assets/Stars/Star1.png").convert_alpha(), (10, 10)),
]

starCoords=[]
for x in range(10):
    coord=(rand.randint(10, 530), rand.randint(10, 890))
    changeCoord=False
    for star in starCoords:
        if abs(star[0][0]-coord[0])+abs(star[0][1]-coord[1]) < 50:
            changeCoord=True
    while changeCoord:
        coord=(rand.randint(10, 530), rand.randint(10, 890))
        changeCoord=False
        for star in starCoords:
            if abs(star[0][0]-coord[0])+abs(star[0][0]-coord[0]) < 50:
                changeCoord=True
    starCoords.append((coord, 0, 0.5+((rand.randint(0, 1000)-500)/500)))

#homeImage=pg.image.load("Assets/Screens/homeScreen.png").convert()
#homeImage.set_colorkey(homeImage.get_at((0, 0))[:3])

upgradeLock=imageImporter.images["Icons"]["UpgradeLock"][0]
upgradeLock=pg.transform.scale(upgradeLock, (50, 50))
upgradeLock.set_colorkey(upgradeLock.get_at((0, 0))[:3])



upgrade1=imageImporter.images["Icons"]["Upgrade"][0]
upgrade1.set_colorkey(upgrade1.get_at((0, 4))[:3])
upgrade1=pg.transform.scale(upgrade1, (50, 50))

upgrade2=imageImporter.images["Icons"]["Upgrade"][1]
upgrade2.set_colorkey(upgrade2.get_at((0, 4))[:3])
upgrade2=pg.transform.scale(upgrade2, (50, 50))

upgrade3=imageImporter.images["Icons"]["Upgrade"][2]
upgrade3.set_colorkey(upgrade3.get_at((0, 4))[:3])
upgrade3=pg.transform.scale(upgrade3, (50, 50))

upgrade1locked=imageImporter.images["Icons"]["UpgradeLocked"][0]
upgrade1locked.set_colorkey(upgrade1locked.get_at((0, 4))[:3])
upgrade1locked=pg.transform.scale(upgrade1locked, (50, 50))

upgrade2locked=imageImporter.images["Icons"]["UpgradeLocked"][1]
upgrade2locked.set_colorkey(upgrade2locked.get_at((0, 4))[:3])
upgrade2locked=pg.transform.scale(upgrade2locked, (50, 50))

upgrade3locked=imageImporter.images["Icons"]["UpgradeLocked"][2]
upgrade3locked.set_colorkey(upgrade3locked.get_at((0, 4))[:3])
upgrade3locked=pg.transform.scale(upgrade3locked, (50, 50))

upgradeCategoryOpen="none"

coinIcon=imageImporter.images["Projectiles"]["CashPellet"][0]
coinIcon.set_colorkey(coinIcon.get_at((0, 0))[:3])
coinIcon=pg.transform.scale(coinIcon, (9, 9))
coinIconRect = coinIcon.get_rect()


gameFrames=0


import player
import bullet
import boss
import bossMaelstrom
import bossMissile
import coin
import bossMinion

pg.display.set_caption("Space Infernum") 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True




upgrades={
    "Weapon": {
        "description": "The default laser gun.", "upgrades": {
            "Damage": {"name": "More Damage", "description": "Deals more damage to enemies and enemy projectiles.", "level": 0, "cost": [100, 200, 400]},
            "AttackSpeed": {"name": "Faster Shooting", "description": "Allows you to shoot the laser gun faster.", "level": 0, "cost": [100, 225, 500]},
            "LaserSpeed": {"name": "Faster Lasers", "description": "Lasers fired will shoot faster.", "level": 0, "cost": [25, 75, 125]},
            "AimAtMouse": {"name": "Aim At Mouse", "description": "Allows you to aim the players weapon at your mouse.", "level": 0, "cost": [50, 100, 150]}}
    }, 
    "Player": {
        "description": "You, the player.", "upgrades": {
            "Speed": {"name": "More Speed", "description": "Allows you to move and turn faster.", "level": 0, "cost": [75, 100, 175]},
            "Brakes": {"name": "Grippier Brakes", "description": "Allows you to slow down faster.", "level": 0, "cost": [50, 75, 100]},
            "Health": {"name": "Healthier Health", "description": "Gives you more health.", "level": 0, "cost": [200, 350, 600]},
            "SmallerHitbox": {"name": "Stealth", "description": "Allows you to get hit by less projectiles.", "level": 0, "cost": [150, 200, 250]}
 
        }
    },
    "???": {
        "description": "???", "upgrades": {
            "???": {"name": "???", "description": "???", "level": 0, "cost": ["$5"]}
        }
    }
}
#upgrades={"bullets": 2, "extraDamage": 1, "extraSpeed": 2, "shotCooldown": 20}
#speed=upgrades["extraSpeed"]

playerSpawn=(270, 720)
playerVelo=(0, 0)
playerRot=0
playerHealth=20 #20
playerDamage=1
playerShotCooldown=10
playerInitShotCooldown=5
playerControlMethod=1
playerCash=0






userPlayer=player.player(playerSpawn, playerVelo, playerRot, playerHealth, playerDamage, playerShotCooldown, playerInitShotCooldown, screen, playerControlMethod, upgrades, fps, playerCash, True)
#userPlayer.cash=100000
keysDown=[False, False, False, False, False] 
mouseClicked=False
bullets=[]

coins=[]

particles=[]

Boss=boss.boss((275, 60), screen, 0, fps)
bossMaelstroms=[]
bossBullets=[]
bossMissiles=[]
bossMinions=[]

def resetScreens(screen):
    userPlayer.screen=screen
    Boss.screen=screen
    for bul in bullets:
        bul.screen=screen
    for bossBul in bossBullets:
        bossBul.screen=screen
    for mael in bossMaelstroms:
        mael.screen=screen
    for miss in bossMissiles:
        miss.screen=screen
    for minion in bossMinions:
        minion.screen=screen
    for coi in coins:
        coi.screen=screen


def saveSettings():
    with open("settings.save", "wb") as f:
        pkl.dump([fps, userPlayer.controlMethod, Boss.profanityVoicelines, vsync], f)

def loadSettings():
    global fps, screen, vsync
    with open("settings.save", "rb") as f:
        fps, userPlayer.controlMethod, Boss.profanityVoicelines, vsync = pkl.load(f)
    Boss.fps=fps
    userPlayer.fps=fps
    
try: 
    loadSettings()
    size=pg.display.get_window_size()
    #del screen
    pg.display.quit()
    screen = pg.display.set_mode(size, flags=pg.SCALED, vsync=int(vsync))
    pg.display.set_caption("Space Infernum") 
    screen.fill(DARKER_GREY)
    resetScreens(screen)
except:
    print("settings.save not found. Creating it as default")
    saveSettings()

      
# The clock will be used to control how fast the screen updates
clock = pg.time.Clock()




gamePaused=False
onHomeScreen=True
selectingSave=False
inShop=False
showingFailedSign=0
failedSignMessage="Nothing. How tf did u even see this?"
shiftHeld=False




# create a text surface object,
# on which text is drawn on it.



def saveProfile():
    with open("profile.save", "wb") as f:
        pkl.dump([userPlayer.cash, Boss.bossTier, userPlayer.bossTiersBeaten, userPlayer.upgrades], f)

def loadProfile():
    with open("profile.save", "rb") as f:
        userPlayer.cash, Boss.bossTier, userPlayer.bossTiersBeaten, userPlayer.upgrades = pkl.load(f)
    Boss.health=Boss.bossStats[Boss.bossTier]["health"]
    Boss.maxHealth=Boss.bossStats[Boss.bossTier]["maxHealth"]




# -------- Main Program Loop -----------
while carryOn:
    gameFrames+=1
    # --- Main event loop
    for event in pg.event.get(): # User did something
        
        if event.type == pg.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop\
        if event.type == pg.MOUSEBUTTONDOWN:
            mousePos=pg.mouse.get_pos()
            keysDown[4] = True
            channel.play(audio)
            
        if event.type == pg.MOUSEBUTTONUP:
            if gamePaused or onHomeScreen or selectingSave or inShop:
                mouseClicked=True
            keysDown[4] = False
            if not inShop:
                if shopRect.collidepoint(mousePos[0], mousePos[1]) or shopIconRect.collidepoint(mousePos[0], mousePos[1]):
                    inShop=True
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                keysDown[0] = True
            if event.key == pg.K_a:
                keysDown[1] = True
            if event.key == pg.K_w:
                keysDown[2] = True
            if event.key == pg.K_s:
                keysDown[3] = True
            if event.key == pg.K_ESCAPE:
                if inShop: inShop = False
                elif gamePaused or not onHomeScreen:
                    gamePaused = not gamePaused
            if event.key == pg.K_RETURN:
                Boss.startNextBoss=True
                
            
            if event.key == pg.K_SPACE:
                keysDown[4] = True
            if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                shiftHeld=True

        if event.type == pg.KEYUP:
            if event.key == pg.K_d:
                keysDown[0] = False
            if event.key == pg.K_a:
                keysDown[1] = False
            if event.key == pg.K_w:
                keysDown[2] = False
            if event.key == pg.K_s:
                keysDown[3] = False
            if event.key == pg.K_SPACE:
                keysDown[4] = False
            if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                shiftHeld=False
            # if event.key == pg.K_SPACE:
            #     keysDown[4] = False

    screen.fill(DARK_GREY)
    actualFps=clock.get_fps() if clock.get_fps() != 0 else 60
    newStarCoords=[]
    for star in starCoords:
        murderThisStar=False
        secUntilUpdate=star[2]
        starTextureNum=star[1]
        secUntilUpdate-=1/actualFps
        screen.blit(stars[starTextureNum], star[0])
        if secUntilUpdate <= 0:
            secUntilUpdate=0.5
            starTextureNum+=1
            if starTextureNum == 7:
                murderThisStar=True

                coord=(rand.randint(10, 530), rand.randint(10, 890))
                changeCoord=False
                for star in starCoords:
                    if abs(star[0][0]-coord[0])+abs(star[0][1]-coord[1]) < 50:
                        changeCoord=True
                while changeCoord:
                    coord=(rand.randint(10, 530), rand.randint(10, 890))
                    changeCoord=False
                    for star in starCoords:
                        if abs(star[0][0]-coord[0])+abs(star[0][0]-coord[0]) < 50:
                            changeCoord=True
                newStarCoords.append((coord, 0, 0.5))
        if not murderThisStar:
            newStarCoords.append((star[0], starTextureNum, secUntilUpdate))
    starCoords=newStarCoords

    
    if not gamePaused and not onHomeScreen and not selectingSave and not inShop:
        
        
        userPlayer.render()
        Boss.render()

        for coi in coins:
            coi.render()

        for bul in bullets:
            bul.render()
        
        for bossBullet in bossBullets:
            bossBullet.render()
        
        for maelstrom in bossMaelstroms:
            maelstrom.render()
        
        for missile in bossMissiles:
            missile.render()
        
        for minion in bossMinions:
            minion.render()
        
        for part in particles:
            part.render()

        userPlayer.update(keysDown, bullets, particles)
        Boss.update(bossMaelstroms, bullets, bossBullets, bossMissiles, bossMinions, coins, userPlayer)
        
        

        bulletsToKill=[]
        for bul in bullets:
            bul.update(bossMaelstroms, Boss, particles)
            if bul.fuckOff:
                bulletsToKill.append(bul)
        for deadBullet in bulletsToKill:
            bullets.pop(bullets.index(deadBullet))

        coinsToKill=[]
        for coi in coins:
            coi.update(userPlayer)
            if coi.fuckOff:
                coinsToKill.append(coi)
        for deadcoin in coinsToKill:
            coins.pop(coins.index(deadcoin))


        maelstromsToKill=[]
        for maelstrom in bossMaelstroms:
            maelstrom.update(bossBullets)
            if maelstrom.fuckOff:
                maelstromsToKill.append(maelstrom)
        for deadMaelstrom in maelstromsToKill:
            bossMaelstroms.pop(bossMaelstroms.index(deadMaelstrom))
        
        bossBulletToKill=[]
        for bossBullet in bossBullets:
            bossBullet.update(userPlayer, particles)
            if bossBullet.fuckOff:
                bossBulletToKill.append(bossBullet)
        for deadBossBullet in bossBulletToKill:
            bossBullets.pop(bossBullets.index(deadBossBullet))

        bossMissileToKill=[]
        for missile in bossMissiles:
            missile.update(userPlayer, bullets)
            if missile.fuckOff:
                bossMissileToKill.append(missile)
        for deadMissile in bossMissileToKill:
            bossMissiles.pop(bossMissiles.index(deadMissile))

        bossMinionsToKill=[]
        for minion in bossMinions:
            minion.update(userPlayer, bossBullets)
            if minion.fuckOff:
                bossMinionsToKill.append(minion)
        for deadMinion in bossMinionsToKill:
            bossMinions.pop(bossMinions.index(deadMinion))
        
        particlesToKill=[]
        for part in particles:
            part.update()
            if part.fuckOff:
                particlesToKill.append(part)
        for deadPart in particlesToKill:
            particles.pop(particles.index(deadPart))
        # --- Game logic should go here
    
        # --- Drawing code should go here
        # First, clear the screen to white. 
        

        #draw the bullets
        
        
        
        if userPlayer.health < 1:
            #upgrades={"bullets": 2, "extraDamage": 1, "extraSpeed": 3, "shotCooldown": 20}
            #speed=upgrades["extraSpeed"]
            userPlayer=player.player(playerSpawn, playerVelo, playerRot, playerHealth, playerDamage, playerShotCooldown, playerInitShotCooldown, screen, playerControlMethod, userPlayer.upgrades, fps, userPlayer.cash, True)
            keysDown=[False, False, False, False, False] 
            bullets=[]



            #Boss=boss.boss((275, 60), 300, 300, 1, 50, 50, 75, 75, screen, 1)
            Boss.pos=(275, 60)
            Boss.velo=(0, 0)
            Boss.internalTimer=0
            Boss.health=Boss.maxHealth
            Boss.timeUntilNextBoss=5
            if Boss.bossTier == 0:
                if Boss.profanityVoicelines:
                    Boss.audioChannels[6].stop()
                    Boss.audioChannels[6].play(Boss.voicelines["kill"][1])
            else:
                if Boss.profanityVoicelines:
                    Boss.audioChannels[6].stop()
                    Boss.audioChannels[6].play(Boss.voicelines["kill"])


            Boss.movementMode=0 #0: spinny, 1: follow above player, 2: go to random spot
            Boss.timeUntilNextMovement=0
            Boss.movementGoal=Boss.pos
            Boss.bossTier=max(Boss.bossTier-1, 0)
            Boss.health=Boss.bossStats[Boss.bossTier]["health"]
            Boss.maxHealth=Boss.bossStats[Boss.bossTier]["maxHealth"]
            bossMaelstroms=[]
            bossBullets=[]
            bossMissiles=[]
            bossMinions=[]
            particles=[]

        #draw the player
        
        #pg.draw.rect(screen, BLACK, [playerPos[0]-10,playerPos[1]-10,20,20])

        #render the boss
        
        actualFps=clock.get_fps()
        fpsT = costFont.render(f"FPS: {actualFps}", True, WHITE, None)
        fpsTRect = fpsT.get_rect()
        fpsTRect.topleft=(0, 0)
        screen.blit(fpsT, fpsTRect)
        newFps=actualFps
        Boss.fps=newFps
        userPlayer.fps=newFps
        for bul in bullets:
            bul.fps=newFps
        for bossBul in bossBullets:
            bossBul.fps=newFps
        for bossMis in bossMissiles:
            bossMis.fps=newFps
        for bossMael in bossMaelstroms:
            bossMael.fps=newFps
        for bossMin in bossMinions:
            bossMin.fps=newFps
        for part in particles:
            part.fps=newFps

        #render the boss healthbar
        text = font.render(f'Boss Health: {Boss.health}', True, RED, None)
        textRect = text.get_rect()
        textRect.center = (270, 20)
        healthBottom=textRect.bottom

        screen.blit(text, textRect)
        if Boss.bossTier == 4:
            if Boss.invincibilityTimer > 0:
                text = font.render(f'Survive {round(Boss.invincibilityTimer)}s', True, RED, None)
                textRect = text.get_rect()
                textRect.center = (270, 20)
                textRect.top=healthBottom+5

                screen.blit(text, textRect)
        if Boss.startNextBoss:
            text = font.render(f'Next boss in {round(Boss.timeUntilNextBoss/Boss.fps, 2)}s', True, RED, None)
            textRect = text.get_rect()
            textRect.center = (270, 20)
            textRect.top=healthBottom+5

            screen.blit(text, textRect)

        text = font.render(f'Health: {userPlayer.health}', True, RED, None)
        textRect = text.get_rect()
        textRect.center = (270, 800)


        pg.draw.rect(screen, BLACK, [0, 820, 550, 80])

        screen.blit(text, textRect)

        text = smallFont.render(f'Cash: {userPlayer.cash}', True, YELLOW, None)
        textRect = text.get_rect()
        textRect.center = (270, 850)

        screen.blit(text, textRect)

        screen.blit(shop, shopRect)
        screen.blit(shopIcon, shopIconRect)

    elif selectingSave:
        screen.fill(GREY)
        mousePos=pg.mouse.get_pos()

        saveTitle = titleFont.render(f'SAVE SELECTOR', False, WHITE, None)
        saveTitleRect = saveTitle.get_rect()
        saveTitleRect.center = (270, 100)
        screen.blit(saveTitle, saveTitleRect)
        
        back = font.render(f'BACK', False, WHITE, None)
        backRect = back.get_rect()
        backRect.center = (270, 550)

        load = font.render(f'LOAD', False, WHITE, None)
        loadRect = load.get_rect()
        loadRect.center = (270, 250)

        new = font.render(f'NEW SAVE', False, WHITE, None)
        newRect = new.get_rect()
        newRect.center = (270, 400)

        if backRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, backRect)
            if mouseClicked:
                mouseClicked=False
                onHomeScreen=True
                selectingSave=False
        if loadRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, loadRect)
            if mouseClicked:
                mouseClicked=False
                selectingSave=False
                onHomeScreen=False
                try:
                    loadProfile()
                except:
                    print("profile.save not found. Making new save.")
                    saveProfile()
        if newRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, newRect)
            if mouseClicked:
                mouseClicked=False
                selectingSave=False
                onHomeScreen=False
                saveProfile()
        if mouseClicked:
            mouseClicked=False
        screen.blit(back, backRect)
        screen.blit(load, loadRect)
        screen.blit(new, newRect)

    elif inShop:
        screen.fill(GREY)
        if showingFailedSign == 0:
            mousePos=pg.mouse.get_pos()


            text = cashFont.render(f'Cash: {userPlayer.cash}', True, YELLOW, None)
            textRect = text.get_rect()
            textRect.topright = (517, 5)

            coinIconBigger=pg.transform.scale(coinIcon, (18, 18))
            coinIconBiggerRect=coinIconBigger.get_rect()

            coinIconBiggerRect.left = textRect.right+2
            coinIconBiggerRect.centery = textRect.centery

            screen.blit(text, textRect)
            screen.blit(coinIconBigger, coinIconBiggerRect)

            categoryTexts=[]
            categoryNames=list(userPlayer.upgrades.keys())
            categoryNum=0
            for category in userPlayer.upgrades:

                text = font.render(category, True, WHITE, None)
                textRect = text.get_rect()
                categoryNum+=50
                textRect.topleft = (25, categoryNum)
                categoryTexts.append(textRect)
                if upgradeCategoryOpen == category:
                    categoryNum+=350

            categoryNum=0
            for category in categoryTexts:
                categoryName=categoryNames[categoryNum]
                categoryNum+=1
                if category.collidepoint(mousePos[0], mousePos[1]):
                    pg.draw.rect(screen, DARK_GREY, category)
                    if mouseClicked:
                        mouseClicked=False
                        
                        if upgradeCategoryOpen == categoryName:
                            upgradeCategoryOpen = 0
                        else:
                            upgradeCategoryOpen = categoryName
            

            

            categoryNum=0
            openUpgradeIcons=[]
            openUpgradeIconRects=[]
            for category in userPlayer.upgrades:

                text = font.render(category, True, WHITE, None)
                textRect = text.get_rect()
                categoryNum+=50
                textRect.topleft = (25, categoryNum)
                topright=textRect.topright
                screen.blit(text, textRect)
                oldBottom=textRect.bottom

                if upgradeCategoryOpen == category:
                    

                    for upgrade in userPlayer.upgrades[category]["upgrades"]:


                        text = smallFont.render(f'{userPlayer.upgrades[category]["upgrades"][upgrade]["name"]}:', True, WHITE, None)
                        textRectNew = text.get_rect()
                        textRectNew.left = 50
                        textRectNew.centery=oldBottom+75

                        
                        upgrade1Rect=upgrade1.get_rect()
                        cost=userPlayer.upgrades[category]["upgrades"][upgrade]["cost"][0]
                        if shiftHeld:
                            upgrade1CostText=costFont.render(f"sell: {round(cost*0.8)}", True, YELLOW, None)
                        upgrade1CostText=costFont.render(str(cost), True, YELLOW, None)
                        upgrade1CostRect=upgrade1CostText.get_rect()
                        upgrade1Rect.left=250
                        upgrade1CostRect.centerx=upgrade1Rect.centerx-5
                        upgrade1CostRect.y=textRectNew.centery+(upgrade1Rect.height//2)+7
                        upgrade1Rect.centery=textRectNew.centery-(upgrade1CostRect.height//2)
                        coinIconRect.y=upgrade1CostRect.y
                        coinIconRect.left=upgrade1CostRect.right+1
                        screen.blit(coinIcon, coinIconRect)

                        openUpgradeIcons.append((category, upgrade, 0))
                        openUpgradeIconRects.append(upgrade1Rect)
                        

                        
                        

                        if upgrade != "???":
                            upgrade2Rect=upgrade2.get_rect()
                            cost=userPlayer.upgrades[category]["upgrades"][upgrade]["cost"][1]
                            upgrade2CostText=costFont.render(str(cost), True, YELLOW, None)
                            upgrade2CostRect=upgrade2CostText.get_rect()
                            upgrade2Rect.left=330
                            upgrade2CostRect.centerx=upgrade2Rect.centerx-5
                            upgrade2CostRect.y=upgrade1CostRect[1]
                            upgrade2Rect.centery=upgrade1Rect.centery
                            coinIconRect.y=upgrade2CostRect.y
                            coinIconRect.left=upgrade2CostRect.right+1
                            screen.blit(coinIcon, coinIconRect)
                            openUpgradeIcons.append((category, upgrade, 1))
                            openUpgradeIconRects.append(upgrade2Rect)

                            upgrade3Rect=upgrade2.get_rect()
                            cost=userPlayer.upgrades[category]["upgrades"][upgrade]["cost"][2]
                            upgrade3CostText=costFont.render(str(cost), True, YELLOW, None)
                            upgrade3CostRect=upgrade3CostText.get_rect()
                            upgrade3Rect.left=410
                            upgrade3CostRect.centerx=upgrade3Rect.centerx-5
                            upgrade3CostRect.y=upgrade1CostRect[1]
                            upgrade3Rect.centery=upgrade2Rect.centery
                            coinIconRect.y=upgrade3CostRect.y
                            coinIconRect.left=upgrade3CostRect.right+1
                            screen.blit(coinIcon, coinIconRect)
                            pg.draw.circle(screen, DARK_GREY, upgrade2Rect.center, 36)
                            pg.draw.circle(screen, DARK_GREY, upgrade3Rect.center, 36)
                            openUpgradeIcons.append((category, upgrade, 2))
                            openUpgradeIconRects.append(upgrade3Rect)
                        pg.draw.circle(screen, DARK_GREY, upgrade1Rect.center, 36)
                        

                        

                        if userPlayer.upgrades[category]["upgrades"][upgrade]["level"] <= 0:
                            upgradeLock1Rect=upgradeLock.get_rect()
                            upgradeLock1Rect.topleft=upgrade1Rect.topleft
                            pg.draw.circle(screen, DARKER_GREY, upgrade1Rect.center, 36)
                            screen.blit(upgrade1locked, upgrade1Rect)
                            screen.blit(upgradeLock, upgradeLock1Rect)
                        else:
                            screen.blit(upgrade1, upgrade1Rect)
                        screen.blit(upgrade1CostText, upgrade1CostRect)
                        
                        if upgrade != "???":
                            if userPlayer.upgrades[category]["upgrades"][upgrade]["level"] <=1:
                                upgradeLock2Rect=upgradeLock.get_rect()
                                upgradeLock2Rect.topleft=upgrade2Rect.topleft
                                pg.draw.circle(screen, DARKER_GREY, upgrade2Rect.center, 36)
                                screen.blit(upgrade2locked, upgrade2Rect)
                                screen.blit(upgradeLock, upgradeLock2Rect)
                            else:
                                screen.blit(upgrade2, upgrade2Rect)
                            screen.blit(upgrade2CostText, upgrade2CostRect)
                            if userPlayer.upgrades[category]["upgrades"][upgrade]["level"] <=2:
                                upgradeLock3Rect=upgradeLock.get_rect()
                                upgradeLock3Rect.topleft=upgrade3Rect.topleft
                                pg.draw.circle(screen, DARKER_GREY, upgrade3Rect.center, 36)
                                screen.blit(upgrade3locked, upgrade3Rect)
                                screen.blit(upgradeLock, upgradeLock3Rect)
                            else:
                                screen.blit(upgrade3, upgrade3Rect)
                            screen.blit(upgrade3CostText, upgrade3CostRect)
                
                

                        screen.blit(text, textRectNew)

                        oldBottom=textRectNew.bottom+5
                    #adder=oldBottom-textRect.bottom
                    categoryNum+=350

            if mouseClicked:
                for ico in range(len(openUpgradeIcons)):
                    icon=openUpgradeIcons[ico]
                    if userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["name"] != "???":
                        if openUpgradeIconRects[ico].collidepoint(mousePos[0], mousePos[1]):
                            if userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["level"] == icon[2]:
                                if userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["cost"][icon[2]] <= userPlayer.cash:
                                    userPlayer.cash-=userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["cost"][icon[2]]
                                    userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["level"]+=1
                                    saveProfile()
                                else:
                                    showingFailedSign=userPlayer.fps
                                    failedSignMessage="Broke :skull:"
                            elif userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["level"] < icon[2]:
                                showingFailedSign=userPlayer.fps
                                failedSignMessage="Too far ahead"
                            else:
                                if shiftHeld:
                                    userPlayer.cash+=round(userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["cost"][icon[2]]*0.8)
                                    userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["level"]-=1
                                    saveProfile()
                                else:
                                    showingFailedSign=userPlayer.fps
                                    failedSignMessage="Already unlocked"
                    else:
                        showingFailedSign=userPlayer.fps*3
                        failedSignMessage="Nah fuck pay2win"
                mouseClicked=False
            if shiftHeld:
                for ico in range(len(openUpgradeIcons)):
                    icon=openUpgradeIcons[ico]
                    if openUpgradeIconRects[ico].collidepoint(mousePos[0], mousePos[1]):
                        desc = cashFont.render(userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["description"], False, WHITE, None)
                        descRect=desc.get_rect()
                        descRect.center=(270, 800)
                        name = cashFont.render(userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["name"], False, WHITE, None)
                        nameRect=name.get_rect()
                        nameRect.center=(270, 800)
                        nameRect.bottom=descRect.top-5
                        sellBackPrice=round(userPlayer.upgrades[icon[0]]['upgrades'][icon[1]]['cost'][icon[2]]*0.8) if userPlayer.upgrades[icon[0]]["upgrades"][icon[1]]["name"] != "???" else "$4"
                        sellBack = cashFont.render(f"Sell: {sellBackPrice}", False, WHITE, None)
                        sellBackRect=sellBack.get_rect()
                        sellBackRect.center=(270-(coinIconRect.width//2), 800)
                        sellBackRect.bottom=nameRect.top-5
                        coinIconRect.y=sellBackRect.y
                        coinIconRect.left=sellBackRect.right+1
                        screen.blit(coinIcon, coinIconRect)
                        screen.blit(desc, descRect)
                        screen.blit(name, nameRect)
                        screen.blit(sellBack, sellBackRect)
        else:
            showingFailedSign-=1
            text = font.render(failedSignMessage, True, BLACK, None)
            textRect = text.get_rect()
            textRect.center = (270, 450)
            pg.draw.rect(screen, WHITE, [textRect.topleft[0]-5, textRect.topleft[1]-5, textRect.width+10, textRect.height+10])
            screen.blit(text, textRect)

        #openUpgradeIcons[(category, upgrade, 0)]=upgrade1Rect
        if mouseClicked:
            mouseClicked=False
        



    if gamePaused:
        mousePos=pg.mouse.get_pos()

        optionsTitle = titleFont.render(f'SPACE INFERNUM', False, WHITE, None)
        optionsTitleRect = optionsTitle.get_rect()
        optionsTitleRect.center = (270, 100)
        screen.blit(optionsTitle, optionsTitleRect)


        fpsT = font.render(f'FPS: {fps}', False, WHITE, None)
        fpsTRect = fpsT.get_rect()
        fpsTRect.center = (270, 300)

        onOrOff=vsync==1
        vsyncT = font.render(f'Vsync: {onOrOff}', False, WHITE, None)
        vsyncTRect = vsyncT.get_rect()
        vsyncTRect.center = (270, 400)
        

        controls = font.render(f'CONTROLS: {playerControlMethod}', False, WHITE, None)
        controlsRect = controls.get_rect()
        controlsRect.center = (270, 500)

        controlsWarning = costFont.render(f'WARNING: SELECTING CONTROLS 0 IS NOT FULLY TESTED. SOME UPGRADES WILL NOT WORK.', False, WHITE, None)
        controlsWarningRect = controlsWarning.get_rect()
        controlsWarningRect.center = (270, 500)
        controlsWarningRect.top = controlsRect.bottom + 5
        
        
        onOrOff=profanityVoicelines==1
        profanity = font.render(f'PROFANITY VOICELINES: {onOrOff}', False, WHITE, None)
        profanityRect = profanity.get_rect()
        profanityRect.center = (270, 600)
        
        back = font.render(f'BACK', False, WHITE, None)
        backRect = back.get_rect()
        backRect.center = (270, 700)

        exitToHome = font.render(f'EXIT TO HOME', False, WHITE, None)
        exitToHomeRect = exitToHome.get_rect()
        exitToHomeRect.center = (270, 800)
        
        if fpsTRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, fpsTRect)
            if mouseClicked:
                mouseClicked=False
                newFps=0
                if fps == 30: newFps = 60
                if fps == 60: newFps = 120
                if fps == 120: newFps = 144
                if fps == 144: newFps = 240
                if fps == 240: newFps = 30
                Boss.fps=newFps
                userPlayer.fps=newFps
                for bul in bullets:
                    bul.fps=newFps
                for bossBul in bossBullets:
                    bossBul.fps=newFps
                for bossMis in bossMissiles:
                    bossMis.fps=newFps
                for bossMael in bossMaelstroms:
                    bossMael.fps=newFps
                for bossMin in bossMinions:
                    bossMin.fps=newFps
                fps=newFps
        
        if vsyncTRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, vsyncTRect)
            if mouseClicked:
                mouseClicked=False
                vsync = not vsync
                #del screen
                pg.display.quit()
                screen = pg.display.set_mode(size, flags=pg.SCALED, vsync=int(vsync))
                pg.display.set_caption("Space Infernum") 
                resetScreens(screen)
                
        
        if controlsRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, controlsRect)
            if mouseClicked:
                mouseClicked=False
                if playerControlMethod == 1: playerControlMethod = 0
                else:playerControlMethod=1
                userPlayer.controlMethod=playerControlMethod
                
        
        if profanityRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, profanityRect)
            if mouseClicked:
                mouseClicked=False
                if profanityVoicelines == 1: profanityVoicelines = 0
                else:profanityVoicelines=1
                
        
        if backRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, backRect)
            if mouseClicked:
                mouseClicked=False
                gamePaused=False
                saveSettings()
                
        if not onHomeScreen:
            if exitToHomeRect.collidepoint(mousePos[0], mousePos[1]):
                pg.draw.rect(screen, DARKER_GREY, exitToHomeRect)
                if mouseClicked:
                    mouseClicked=False
                    gamePaused=False
                    onHomeScreen=True
                    userPlayer=player.player(playerSpawn, playerVelo, playerRot, playerHealth, playerDamage, playerShotCooldown, playerInitShotCooldown, screen, playerControlMethod, userPlayer.upgrades, fps, userPlayer.cash, True)
                    keysDown=[False, False, False, False, False] 
                    bullets=[]



                    #Boss=boss.boss((275, 60), 300, 300, 1, 50, 50, 75, 75, screen, 1)
                    Boss.pos=(275, 60)
                    Boss.velo=(0, 0)
                    Boss.internalTimer=0
                    Boss.health=Boss.maxHealth

                    Boss.movementMode=0 #0: spinny, 1: follow above player, 2: go to random spot
                    Boss.timeUntilNextMovement=0
                    Boss.movementGoal=Boss.pos
                    #Boss.bossTier=max(Boss.bossTier-1, 0)
                    Boss.health=Boss.bossStats[Boss.bossTier]["health"]
                    Boss.maxHealth=Boss.bossStats[Boss.bossTier]["maxHealth"]
                    bossMaelstroms=[]
                    bossBullets=[]
                    bossMissiles=[]
                    bossMinions=[]
                    particles=[]
                    saveSettings()
                
        if mouseClicked:
            mouseClicked=False
        
        screen.blit(back, backRect)
        screen.blit(profanity, profanityRect)
        screen.blit(controls, controlsRect)
        screen.blit(controlsWarning, controlsWarningRect)
        screen.blit(fpsT, fpsTRect)
        screen.blit(vsyncT, vsyncTRect)
        if not onHomeScreen:
            screen.blit(exitToHome, exitToHomeRect)
                
    elif onHomeScreen:
        #screen.fill(DARK_GREY)

        
        screen.blit(title, titleRect)

        mousePos=pg.mouse.get_pos()

        

        if playRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, playRect)
            if mouseClicked:
                mouseClicked=False
                onHomeScreen=False
                selectingSave=True
        screen.blit(play, playRect)

        
        if optionsRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, optionsRect)
            if mouseClicked:
                mouseClicked=False
                gamePaused=True
        screen.blit(options, optionsRect)
        
        if stopRect.collidepoint(mousePos[0], mousePos[1]):
            pg.draw.rect(screen, DARKER_GREY, stopRect)
            if mouseClicked:
                mouseClicked=False
                saveSettings()
                pg.quit()
                quit()
        screen.blit(stop, stopRect)
        if mouseClicked:
            mouseClicked=False

        
        


        #screen.blit(homeImage, (0, 0))



     # --- Go ahead and update the screen with what we've drawn.
    
        
    
    clock.tick(fps)
    pg.display.flip()
    pg.display.update()
     
     # --- Limit to 120 frames per second
    
 
#Once we have exited the main program loop we can stop the game engine:
saveSettings()
pg.quit()