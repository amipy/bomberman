import copy

from Model.objects import *


class Field:
    CELL_EMPTY = 0
    CELL_DESTR_BRICK = 2
    CELL_INDESTR_BRICK = 1
    CELL_START = 3
    CELL_FINISH = 4
    CELL_HIDDEN_FINISH = 24
    CELL_ENEMY1 = 5
    DESTRUCTIBLES = [2, 0, 3, 24, 4, 5]
    EXPL_PASSABLE = [3, 4, 5]
    UNPASSABLE_BY_GOBJECTS = [1, 2]

    GAME_STATE_PLAYING = 0
    GAME_STATE_FINISH = 1
    GAME_STATE_DIED = 2


    _player = None
    _tileSize = 0
    _bombData = []
    _mineData = []
    _explosions = []
    _enemies = []
    cellForEdit = [0, 0]


    def __init__(self, width, height):
        self._field = [[0 for i in range(0,width)] for i in range(0,height)]
        self._startLevelField = [[0 for i in range(0,width)] for i in range(0,height)]

    def loadFromFile(filename, tileSize):

        '''
        0 is an empty tile without any parameters.
        1 is an indestructible tile without any parameters.
        2 is a destructible tile with 1 parameter.
            Parameter 1 decides what is inside the tile.
                0 means nothing is inside. This can also be done by not mentioning a parameter.
                1 means a heart.
                2 means a bomb strength.
                3 means a bomb count upgrade.
                4 means a heart count upgrade.
                5 means a random item.
                6 means an exit door.
        3 is a empty tile that serves as the starting platform.
        4 is a enemy spawn tile with 4 parameters.
            Parameter 1 describes the movement direction of the movement.
                0 means left to right.
                1 means up and down.
            Parameter 2 describes the movement distance in direction 1.
            Parameter 3 describes the movement distance in direction 2.
            Parameter 4 describes the enemy speed in tiles per second.
            Parameter 5 describes if the enemy can move through walls.
                0 means the enemy cannot pass thorough any tiles.
                1 means the enemy can pass through destructible tiles only.
                2 means the enemy can pass through indestructible tile only.
                3 means the enemy can pass through all types of tiles.
        5 is an enemy spawn tile that spawns a smart enemy.
            Parameter 1 describes the speed in tiles per second.
            Parameter 2 describes is the enemy can move through walls.
                0 means the enemy cannot pass thorough any tiles.
                1 means the enemy can pass through destructible tiles only.
                2 means the enemy can pass through indestructible tile only.
                3 means the enemy can pass through all types of tiles.
                          '''

        field = []
        with open(filename, "r") as file:
            for line in file:
                field.append([int(i) for i in line.split()])

        map = Field(0,0)
        map._field = field
        map._startLevelField = copy.deepcopy(field)
        map._tileSize = tileSize
        map._spawnPlayer()
        map._spawnEnemies()
        return map

    def saveFieldToFile(field, filename):
        with open(filename, "w") as f:
            for line in field._field:
                f.write(" ".join([str(i) for i in line]) + "\n")


    def createEmptyField(width, height):
        return Field(width, height)

    def playerIsVisibleByEnemy(self, enemy):
        return GameObject.getDistance(self._player, enemy) < 100

    def getField(self):
        return self._field

    def getPlayerPosition(self):
        return self._player.getPosition()

    def getPlayer(self):
        return self._player

    def getSize(self):
        return len(self._field[0]),len(self._field)

    def _spawnPlayer(self):
        found=False
        for y,i in enumerate(self._field):
            for x,c in enumerate(i):
                if c==self.CELL_START:
                    found=True
                    break
            if found: break

        tSize = self._tileSize
        self._player = Player(x*tSize+tSize//2, y*tSize+tSize//2)

    def moveCellForEditRight(self):
        if self.cellForEdit[0] < len(self._field[0])-1:
            self.cellForEdit[0] += 1

    def moveCellForEditLeft(self):
        if self.cellForEdit[0] > 0:
            self.cellForEdit[0] -= 1

    def moveCellForEditUp(self):
        if self.cellForEdit[1] > 0:
            self.cellForEdit[1] -= 1

    def moveCellForEditDown(self):
        if self.cellForEdit[1] < len(self._field)-1:
            self.cellForEdit[1] += 1

    def changeCell(self, step):
        x = self.cellForEdit[0]
        y = self.cellForEdit[1]
        self._field[y][x] += step
        if self._field[y][x] < 0:
            self._field[y][x] = 0
        #print(f"New cell value is {self._field[y][x]}")


    def movePlayerLeft(self):
        collisionPoint1 = (self._player.getLeftBorder() - 1, self._player.getTopBorder())
        collisionPoint2 = (self._player.getLeftBorder() - 1, self._player.getBottomBorder())
        mapCoordinate1 = self.pixelCoordToMapCoord(collisionPoint1)
        mapCoordinate2 = self.pixelCoordToMapCoord(collisionPoint2)
        if not (mapCoordinate1[0] == -1):
            cell1 = self._field[mapCoordinate1[1]][mapCoordinate1[0]]
            cell2 = self._field[mapCoordinate2[1]][mapCoordinate2[0]]
            if self.isPassable(cell1) and self.isPassable(cell2):
                self._player.move(-1, 0)

    def movePlayerRight(self):
        collisionPoint1 = (self._player.getRightBorder() + 1, self._player.getTopBorder())
        collisionPoint2 = (self._player.getRightBorder() + 1, self._player.getBottomBorder())
        mapCoordinate1 = self.pixelCoordToMapCoord(collisionPoint1)
        mapCoordinate2 = self.pixelCoordToMapCoord(collisionPoint2)
        if not (mapCoordinate1[0] == self.getSize()[0]):
            cell1 = self._field[mapCoordinate1[1]][mapCoordinate1[0]]
            cell2 = self._field[mapCoordinate2[1]][mapCoordinate2[0]]
            if self.isPassable(cell1) and self.isPassable(cell2):
                self._player.move(1, 0)

    def movePlayerUp(self):
        collisionPoint1 = (self._player.getLeftBorder(), self._player.getTopBorder()-1)
        collisionPoint2 = (self._player.getRightBorder(), self._player.getTopBorder()-1)
        mapCoordinate1 = self.pixelCoordToMapCoord(collisionPoint1)
        mapCoordinate2 = self.pixelCoordToMapCoord(collisionPoint2)
        if not (mapCoordinate1[1] == -1):
            cell1 = self._field[mapCoordinate1[1]][mapCoordinate1[0]]
            cell2 = self._field[mapCoordinate2[1]][mapCoordinate2[0]]
            if self.isPassable(cell1) and self.isPassable(cell2):
                self._player.move(0, -1)

    def movePlayerDown(self):
        collisionPoint1 = (self._player.getRightBorder(), self._player.getBottomBorder()+1)
        collisionPoint2 = (self._player.getLeftBorder(), self._player.getBottomBorder()+1)
        mapCoordinate1 = self.pixelCoordToMapCoord(collisionPoint1)
        mapCoordinate2 = self.pixelCoordToMapCoord(collisionPoint2)
        if not (mapCoordinate1[1] == self.getSize()[1]):
            cell1 = self._field[mapCoordinate1[1]][mapCoordinate1[0]]
            cell2 = self._field[mapCoordinate2[1]][mapCoordinate2[0]]
            if self.isPassable(cell1) and self.isPassable(cell2):
                self._player.move(0, 1)

    def objectCanMoveRight(self, obj:GameObject, steps):
        collisionPoint = (obj.getRightBorder() + steps, obj.getPosition()[1])
        cell = self.pixelCoordToMapCoord(collisionPoint)
        return not self._wrongCoordinates(*cell) and self.isPassable(self.getCell(*cell))

    def objectCanMoveLeft(self, obj:GameObject, steps):
        collisionPoint = (obj.getLeftBorder() - steps, obj.getPosition()[1])
        cell = self.pixelCoordToMapCoord(collisionPoint)
        return not self._wrongCoordinates(*cell) and self.isPassable(self.getCell(*cell))

    def objectCanMoveUp(self, obj:GameObject, steps):
        collisionPoint = ( obj.getPosition()[0], obj.getTopBorder() - steps)
        cell = self.pixelCoordToMapCoord(collisionPoint)
        return not self._wrongCoordinates(*cell) and self.isPassable(self.getCell(*cell))

    def objectCanMoveDown(self, obj: GameObject, steps):
        collisionPoint = (obj.getPosition()[0], obj.getBottomBorder() + steps)
        cell = self.pixelCoordToMapCoord(collisionPoint)
        return not self._wrongCoordinates(*cell) and self.isPassable(self.getCell(*cell))

    def objectOnBomb(self, obj):
        for b in self._bombData:
            if GameObject.areCollided(b[1], obj):
                return True
        return False

    def isPassable(self, cell):
        return cell not in self.UNPASSABLE_BY_GOBJECTS
        # return cell != 1 and cell != 2

    def getCell(self, x, y):
        return self._field[y][x]

    def _isDestructible(self, cell):
        x, y = cell
        if self._wrongCoordinates(x, y):
            return
        cell = self._field[y][x]
        return cell in self.DESTRUCTIBLES

    def pixelCoordToMapCoord(self, point):
        return int(point[0] // self._tileSize), int(point[1] // self._tileSize)

    def mapCoordToPixelCoord(self, point):
        tSize = self._tileSize
        return point[0]*tSize+tSize//2, point[1]*tSize+tSize//2

    def placeBomb(self):
        mapCoordinate = self.pixelCoordToMapCoord(self._player.getPosition())
        for i in self._bombData:
            if i[0]==mapCoordinate:
                return
        pixelCoordinate = self.mapCoordToPixelCoord(mapCoordinate)
        b = Bomb(pixelCoordinate[0], pixelCoordinate[1], power=30)
        self._bombData.append([mapCoordinate, b])

    def placeQbomb(self):
        mapCoordinate = self.pixelCoordToMapCoord(self._player.getPosition())
        for i in self._bombData:
            if i[0] == mapCoordinate:
                return
        pixelCoordinate = self.mapCoordToPixelCoord(mapCoordinate)
        b = Bomb(pixelCoordinate[0], pixelCoordinate[1], power=30, lifetime=Bomb.QUICK_BOMB)
        self._bombData.append([mapCoordinate, b])

    def placeMine(self):
        mapCoordinate = self.pixelCoordToMapCoord(self._player.getPosition())
        for i in self._mineData:
            if i[0] == mapCoordinate:
                return
        pixelCoordinate = self.mapCoordToPixelCoord(mapCoordinate)
        b = Mine(pixelCoordinate[0], pixelCoordinate[1], power=0)
        self._mineData.append([mapCoordinate, b])

    def setCell(self, x, y, cell):
        if self._wrongCoordinates(x, y):
            return
        self._field[y][x] = cell

# ***p**



    def process(self):
        xplayer, yplayer = self.getPlayerPosition()
        xplayer, yplayer = self.pixelCoordToMapCoord((xplayer, yplayer))
        cell = self._field[yplayer][xplayer]
        for b in self._bombData:
            if b[1].shouldExplode():
                up=True
                down=True
                left=True
                right=True
                cell = b[0]
                for i in range(1,b[1].getPower()+1):
                    right = self._process_expl_way((cell[0] + i, cell[1]), right)
                    left = self._process_expl_way((cell[0] - i, cell[1]), left)
                    up = self._process_expl_way((cell[0], cell[1] - i), up)
                    down = self._process_expl_way((cell[0], cell[1] + i), down)
                self._explosions.append(Explosion(self.mapCoordToPixelCoord((cell[0], cell[1]))))
                self._bombData.remove(b)
        for b in self._mineData:
            if b[1].canExplode():
                for enem in self._enemies:
                    #enemx, enemy = enem.getPosition()
                    #minex, m iney = b[1].getPosition()
                    if GameObject.areCollided(b[1], enem):
                        up=True
                        down=True
                        left=True
                        right=True
                        cell = b[0]
                        for i in range(1,b[1].getPower()+1):
                            right = self._process_expl_way((cell[0] + i, cell[1]), right)
                            left = self._process_expl_way((cell[0] - i, cell[1]), left)
                            up = self._process_expl_way((cell[0], cell[1] - i), up)
                            down = self._process_expl_way((cell[0], cell[1] + i), down)
                        self._explosions.append(Explosion(self.mapCoordToPixelCoord((cell[0], cell[1]))))
                        self._mineData.remove(b)
                if GameObject.areCollided(self._player, b[1]):
                    up = True
                    down = True
                    left = True
                    right = True
                    cell = b[0]
                    for i in range(1, b[1].getPower() + 1):
                        right = self._process_expl_way((cell[0] + i, cell[1]), right)
                        left = self._process_expl_way((cell[0] - i, cell[1]), left)
                        up = self._process_expl_way((cell[0], cell[1] - i), up)
                        down = self._process_expl_way((cell[0], cell[1] + i), down)
                    self._explosions.append(Explosion(self.mapCoordToPixelCoord((cell[0], cell[1]))))
                    self._mineData.remove(b)
        for b in self._explosions:
            if self.pixelCoordToMapCoord(b.getPosition()) == (xplayer,yplayer):
                return self.GAME_STATE_DIED
            if b.shouldExpire():
                self._explosions.remove(b)
            for enemie in self._enemies:
                #if self.pixelCoordToMapCoord(enemie.getPosition()) == self.pixelCoordToMapCoord(b.getPosition()):
                if GameObject.areCollided(enemie, b):
                    self._enemies.remove(enemie)
        for enemie in self._enemies:
            enemie.process(self)
            if GameObject.areCollided(enemie, self._player):
                return self.GAME_STATE_DIED
            # if self.pixelCoordToMapCoord(enemie.getPosition()) == (xplayer, yplayer):
            #     return self.GAME_STATE_DIED
        if cell==4:
            return self.GAME_STATE_FINISH
        return self.GAME_STATE_PLAYING

    def reload_level(self):
        self._field = copy.deepcopy(self._startLevelField)
        self._spawnPlayer()
        self._explosions.clear()
        self._bombData.clear()
        self._mineData.clear()

        self._enemies.clear()
        self._spawnEnemies()

    def _process_expl_way(self, nextCell, key_variable):
        if self._isDestructible(nextCell):
            if key_variable:
                if not self._cellExplPassable(nextCell):
                    if self.getCell(*nextCell) == self.CELL_HIDDEN_FINISH:
                        self.setCell(nextCell[0], nextCell[1], 4)
                    else:
                        self.setCell(nextCell[0], nextCell[1], 0)
                self._explosions.append(Explosion(self.mapCoordToPixelCoord(nextCell)))
        else:
            return False
        return key_variable

    def getBombs(self):
        return self._bombData

    def getMines(self):
        return self._mineData

    def getExplosions(self):
        return self._explosions

    def _wrongCoordinates(self, x, y):
        return x < 0 or x >= self.getSize()[0] or y < 0 or y >= self.getSize()[1]

    def _cellExplPassable(self, cell):
        x, y = cell
        if self._wrongCoordinates(x, y):
            return
        cell = self._field[y][x]
        return cell in self.EXPL_PASSABLE

    def getEnemies(self):
        return self._enemies

    def _spawnEnemies(self):
        for y,i in enumerate(self._field):
            for x,c in enumerate(i):
                if c==self.CELL_ENEMY1:
                    pos = self.mapCoordToPixelCoord((x, y))
                    self._enemies.append(Enemy(pos[0], pos[1], 0, self._tileSize*max(self.getSize())))

