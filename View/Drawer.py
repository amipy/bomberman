import pygame
from View.Block import Block
from View.GameObject import GameObject


class Drawer:
    invisibleBlocks = [3, 5]

    def __init__(self, screen, tileSize):
        self._screen = screen
        self._topIndent = 40
        self._leftIndent = 40
        self._cellSizePx = tileSize
        self._font = pygame.sysfont.SysFont("Arial", 12)

    def setFieldModel(self, model):
        self._field = model

    def clearScreen(self):
        self._screen.fill((0,0,0))

    def drawField(self):
        map = self._field.getField()
        x,y=self._field.getSize()

        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                if cell not in self.invisibleBlocks:
                    Block.draw(self._screen, cell, (self._leftIndent + x * self._cellSizePx, self._topIndent + y * self._cellSizePx), self._cellSizePx)

        bombs=self._field.getBombs()
        for i in bombs:
            pos=i[1].getPosition()
            GameObject.drawBomb(self._screen,(self._leftIndent+pos[0], self._topIndent+pos[1]))

        mines = self._field.getMines()
        for i in mines:
            pos = i[1].getPosition()
            GameObject.drawMine(self._screen, (self._leftIndent + pos[0], self._topIndent + pos[1]))

        explosions = self._field.getExplosions()
        for i in explosions:
            pos=i.getPosition()
            GameObject.drawExplosion(self._screen,(self._leftIndent+pos[0], self._topIndent+pos[1]))

        enemies = self._field.getEnemies()
        for i in enemies:
            pos = i.getPosition()
            GameObject.drawEnemy(self._screen, (self._leftIndent + pos[0], self._topIndent + pos[1]), 0)

        player = self._field.getPlayerPosition()
        GameObject.drawPlayer(self._screen, (self._leftIndent + player[0], self._topIndent + player[1]))

        pygame.draw.rect(self._screen, (0, 0, 150),(self._leftIndent, self._topIndent, (x+1) * self._cellSizePx, (y+1) * self._cellSizePx), 3)

    def drawInfo(self, selected):
        if selected==0:
            GameObject.drawBomb(self._screen, (16,16),)
        if selected==1:
            GameObject.drawMine(self._screen, (16, 16), )
        if selected==2:
            GameObject.drawQBomb(self._screen, (16, 16), )

    def drawFieldForEdit(self):
        map = self._field.getField()
        x, y = self._field.getSize()


        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                Block.draw(self._screen, cell,
                           (self._leftIndent + x * self._cellSizePx, self._topIndent + y * self._cellSizePx),
                           self._cellSizePx)

        cell = self._field.cellForEdit
        pygame.draw.rect(self._screen, (255, 0, 0),
                         (self._leftIndent + cell[0]*self._cellSizePx, self._topIndent + cell[1]*self._cellSizePx, self._cellSizePx,self._cellSizePx), 2)
        pygame.draw.rect(self._screen, (0, 0, 150),
                         (self._leftIndent, self._topIndent, (x + 1) * self._cellSizePx, (y + 1) * self._cellSizePx), 3)

    def drawInfoForEdit(self):
        cell = self._field.cellForEdit
        cellValue = self._field.getCell(cell[0],cell[1])
        surface = self._font.render(f"Current pos: {cell[0]},{cell[1]}", False, (0, 0, 200))
        self._screen.blit(surface, (self._screen.get_width() - surface.get_width() - 10, 30))
        surface = self._font.render(f"Current value: {cellValue}", False, (0,0,200))
        self._screen.blit(surface, (self._screen.get_width() - surface.get_width() - 10, 50))