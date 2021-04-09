import pygame


class GameObject:
    def loadResources():
        GameObject.playerImg = pygame.image.load("Resources/player.png").convert_alpha()
        GameObject.bombImg = pygame.image.load("Resources/bomb20.png").convert_alpha()
        GameObject.explosionImg = pygame.image.load("Resources/explosion30_1.png").convert_alpha()
        GameObject.enemy = pygame.image.load("Resources/enemy.png").convert_alpha()
        GameObject.mineImg = pygame.image.load("Resources/mine.png").convert_alpha()
        GameObject.qbomb = pygame.image.load("Resources/qbomb.png").convert_alpha()

    def drawPlayer(screen, pos):
        #pygame.draw.circle(screen, (200, 0, 10), pos, 6)
        screen.blit(GameObject.playerImg, (pos[0]-GameObject.playerImg.get_width()//2, pos[1]-GameObject.playerImg.get_height()//2))

    def drawEnemy(screen, pos, kind):
        screen.blit(GameObject.enemy,
                    (pos[0] - GameObject.enemy.get_width() // 2, pos[1] - GameObject.enemy.get_height() // 2))

    def drawBomb(screen, pos):
        screen.blit(GameObject.bombImg,(pos[0] - GameObject.bombImg.get_width() // 2, pos[1] - GameObject.bombImg.get_height() // 2))

    def drawMine(screen, pos):
        screen.blit(GameObject.mineImg,(pos[0] - GameObject.mineImg.get_width() // 2, pos[1] - GameObject.mineImg.get_height() // 2))

    def drawExplosion(screen, pos):
        screen.blit(GameObject.explosionImg,(pos[0] - GameObject.explosionImg.get_width() // 2, pos[1] - GameObject.explosionImg.get_height() // 2))

    def drawQBomb(screen, pos):
        screen.blit(GameObject.qbomb,(pos[0] - GameObject.qbomb.get_width() // 2, pos[1] - GameObject.qbomb.get_height() // 2))