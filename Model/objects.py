import math
import time, random


class GameObject:
    def __init__(self, x, y):
        self._x, self._y = x, y

    def getPosition(self):
        return self._x, self._y

    def setPosition(self, x, y):
        self._x = x
        self._y = y

    def move(self, dx, dy):
        self._x += dx
        self._y += dy

    def setBorders(self, radius):
        self._radius = radius

    def getRadius(self):
        return self._radius

    def getLeftBorder(self):
        return self._x - self._radius

    def getRightBorder(self):
        return self._x + self._radius

    def getTopBorder(self):
        return self._y - self._radius

    def getBottomBorder(self):
        return self._y + self._radius

    @staticmethod
    def areCollided(o1, o2):
        dist = GameObject.getDistance(o1, o2)
        return o1.getRadius()+o2.getRadius() > dist

    @staticmethod
    def getDistance(o1, o2):
        return math.sqrt((o1._x - o2._x) ** 2 + (o1._y - o2._y) ** 2)


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.setBorders(10)


class Enemy(GameObject):
    DIR_RIGHT = 0
    DIR_LEFT=1
    DIR_UP=2
    DIR_DOWN=3

    def __init__(self, x, y, kind, maxsteps):
        super().__init__(x, y)
        self.setBorders(16)
        self._kind = kind
        self._speed = 0.7
        self._direction= self.DIR_DOWN
        self._fieldsize=maxsteps
        self._distance=random.randint(10, self._fieldsize)
        #self.direction=random.randint(0,1)

    def process(self, field):
        self._distance -= 1
        pl = field.getPlayer()
        if field.objectOnBomb(self):
            if self._direction == self.DIR_RIGHT:
                self.move(-2*self._speed, 0)
                self._direction = self.DIR_LEFT
            if self._direction == self.DIR_LEFT:
                self.move(2*self._speed, 0)
                self._direction = self.DIR_RIGHT
            if self._direction == self.DIR_UP:
                self.move(0,2*self._speed)
                self._direction = self.DIR_DOWN
            if self._direction == self.DIR_DOWN:
                self.move(0,-2*self._speed)
                self._direction = self.DIR_UP
            return

        if field.playerIsVisibleByEnemy(self):
            if pl.getPosition()[0] < self._x and field.objectCanMoveLeft(self, self._speed):
                self.move(-self._speed, 0)
            elif pl.getPosition()[0] > self._x and field.objectCanMoveRight(self, self._speed):
                self.move(self._speed, 0)
            if pl.getPosition()[1] < self._y and field.objectCanMoveUp(self, self._speed):
                self.move(0,-self._speed)
            elif pl.getPosition()[1] > self._y and field.objectCanMoveDown(self, self._speed):
                self.move(0,self._speed)
            return



        if self._distance == 0:
            self._direction = random.randint(0, 3)
            self._distance = random.randint(10, self._fieldsize)
        if self._direction == self.DIR_RIGHT and field.objectCanMoveRight(self, self._speed):
            self.move(self._speed, 0)
        elif self._direction == self.DIR_LEFT and field.objectCanMoveLeft(self, self._speed):
            self.move(-self._speed, 0)
        elif self._direction == self.DIR_UP and field.objectCanMoveUp(self, self._speed):
            self.move(0, -self._speed)
        elif self._direction == self.DIR_DOWN and field.objectCanMoveDown(self, self._speed):
            self.move(0, self._speed)
        else:
            self._direction = random.randint(0, 3)
            self._distance = random.randint(10, self._fieldsize)


class Bomb(GameObject):
    DEFAULT_BOMB = 3000
    QUICK_BOMB = 1500

    def __init__(self, x, y, power=1, lifetime=DEFAULT_BOMB):
        super().__init__(x, y)
        self.setBorders(10)
        self._placeTime = int(round(time.time() * 1000))
        self._explodeTime = self._placeTime + lifetime
        self._power = power
        #print(self._placeTime, self._explodeTime)

    def shouldExplode(self):
        curTume = int(round(time.time() * 1000))
        return curTume > self._explodeTime

    def getPower(self):
        return self._power

class Explosion(GameObject):
    EXPLOSION = 1000
    def __init__(self, pos, power=1):
        super().__init__(pos[0], pos[1])
        self.setBorders(10)
        self._placeTime = int(round(time.time() * 1000))
        self._expireTime = self._placeTime + self.EXPLOSION

    def shouldExpire(self):
        curTume = int(round(time.time() * 1000))
        return curTume > self._expireTime

class Mine(GameObject):

    def __init__(self, x, y, power=1):
        super().__init__(x, y)
        self.setBorders(10)
        self._power = power
        self._placeTime = int(round(time.time() * 1000))
        self._minExplodeTime = self._placeTime + 1500

    def canExplode(self):
        curTume = int(round(time.time() * 1000))
        return curTume > self._minExplodeTime

    def getPower(self):
        return self._power