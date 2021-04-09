import pygame


class Block(object):


    def loadResources():
        Block.wall1Img = pygame.image.load("Resources/Wall1.png")
        Block.wall2Img = pygame.image.load("Resources/Wall2.png")
        Block.playerStartImg = pygame.image.load("Resources/playerstart.png")
        Block.playerStartImg = pygame.transform.scale(Block.playerStartImg, (Block.playerStartImg.get_width()//2, Block.playerStartImg.get_height()//2))
        Block.playerEndImg = pygame.image.load("Resources/goal.png")
        Block.playerEndImg = pygame.transform.scale(Block.playerEndImg, (Block.playerEndImg.get_width() // 2, Block.playerEndImg.get_height() // 2))
        Block.enemyImg = pygame.image.load("Resources/enemy.png")


    def draw(screen, cell, coordinates, sizePx):
        cellRect = (coordinates[0], coordinates[1], sizePx, sizePx)
        if cell == 1:
            screen.blit(Block.wall2Img, coordinates)
        if cell == 2:
            screen.blit(Block.wall1Img, coordinates)
        if cell == 3:
            screen.blit(Block.playerStartImg, coordinates)
        if cell == 4:
            screen.blit(Block.playerEndImg, coordinates)
        if cell == 5:
            screen.blit(Block.enemyImg, coordinates)
        if cell == 200:
            pygame.draw.rect(screen, (60, 60, 60), cellRect)
