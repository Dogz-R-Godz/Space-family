import pygame as pg

#img = pg.image.load('cn_pygame.png')
#img


images={
    "Player": {
        "noDamage": {"Idle":        [pg.image.load('Assets/Player/noDamage/PlayerIdle.png').convert()],
                    "Accelerating": [pg.image.load('Assets/Player/noDamage/PlayerAccelerating1.png').convert(), 
                                     pg.image.load('Assets/Player/noDamage/PlayerAccelerating2.png').convert()],
                    "Moving":       [pg.image.load('Assets/Player/noDamage/PlayerMoving1.png').convert(),
                                     pg.image.load('Assets/Player/noDamage/PlayerMoving2.png').convert(),
                                     pg.image.load('Assets/Player/noDamage/PlayerMoving3.png').convert(),
                                     pg.image.load('Assets/Player/noDamage/PlayerMoving4.png').convert(),
                                     pg.image.load('Assets/Player/noDamage/PlayerMoving5.png').convert()]}, 

        "muchDamage": {"Idle":      [pg.image.load('Assets/Player/muchDamage/PlayerIdle.png').convert()],
                    "Accelerating": [pg.image.load('Assets/Player/muchDamage/PlayerAccelerating1.png').convert(), 
                                     pg.image.load('Assets/Player/muchDamage/PlayerAccelerating2.png').convert()],
                    "Moving":       [pg.image.load('Assets/Player/muchDamage/PlayerMoving1.png').convert(),
                                     pg.image.load('Assets/Player/muchDamage/PlayerMoving2.png').convert(),
                                     pg.image.load('Assets/Player/muchDamage/PlayerMoving3.png').convert(),
                                     pg.image.load('Assets/Player/muchDamage/PlayerMoving4.png').convert(),
                                     pg.image.load('Assets/Player/muchDamage/PlayerMoving5.png').convert()]}
    }, 
    "Projectiles": {
        "PlayerBullet": [pg.image.load('Assets/Projectiles/PlayerBullet1.png').convert(), 
                         pg.image.load('Assets/Projectiles/PlayerBullet2.png').convert(), 
                         pg.image.load('Assets/Projectiles/PlayerBullet3.png').convert()],
        "BossBullet":   [pg.image.load('Assets/Projectiles/BossBullet1.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossBullet2.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossBullet3.png').convert()],
        "BossPellet":   [pg.image.load('Assets/Projectiles/BossPellet1.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossPellet2.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossPellet3.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossPellet4.png').convert()],
        "BossMaelstrom":[pg.image.load('Assets/Projectiles/BossMaelstromSpin1.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossMaelstromSpin2.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossMaelstromSpin3.png').convert()],
        "BossMissile":  [pg.image.load('Assets/Projectiles/BossMissile1.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossMissile2.png').convert(), 
                         pg.image.load('Assets/Projectiles/BossMissile3.png').convert()],
        "CashPellet":   [pg.image.load('Assets/Projectiles/Coin.png').convert()],
    },
    "Boss": {
        "noDamage": [pg.image.load('Assets/Boss/noDamage/BossIdlet1.png').convert_alpha(),
                     pg.image.load('Assets/Boss/noDamage/BossIdlet2.png').convert_alpha(),
                     pg.image.load('Assets/Boss/noDamage/BossIdlet3.png').convert_alpha(),
                     pg.image.load('Assets/Boss/noDamage/BossIdlet4.png').convert_alpha(),
                     pg.image.load('Assets/Boss/noDamage/BossIdlet5.png').convert_alpha()], 
        "muchDamage": [pg.image.load('Assets/Boss/muchDamage/BossDamageMask.png').convert_alpha()],
        "minion": [pg.image.load('Assets/MinionTurrets/MinionTurret.png').convert()]
    },
    "Icons": {
        "UpgradeLock": [pg.image.load('Assets/Icons/UpgradeLock.png').convert_alpha()],
        "Upgrade": [pg.image.load('Assets/Icons/upgrade1.png').convert(),
                    pg.image.load('Assets/Icons/upgrade2.png').convert(),
                    pg.image.load('Assets/Icons/upgrade3.png').convert()], 
        "UpgradeLocked": [pg.image.load('Assets/Icons/upgrade1locked.png').convert(),
                    pg.image.load('Assets/Icons/upgrade2locked.png').convert(),
                    pg.image.load('Assets/Icons/upgrade3locked.png').convert()]
    }
}

# images2={}

# for x in images:
#     for y in images[x]:
#         for z in images[x][y]:
#             for a in range(len(images[x][y][z])):
#                 images[x][y][z][a] = pg.transform.scale(images[x][y][z][a], (images[x][y][z][a].get_size()[0]*2, images[x][y][z][a].get_size()[1]*2))
                