class RPGCharacter:
    def __init__(self, name, hp, attackPower, defense, level=1):
        self._name = name
        self._hp = hp
        self._attackPower = attackPower
        self._defense = defense
        self._level = level
        self._exp = 0

    def attack(self, otherCharacter):
        damage = max(self._attackPower - otherCharacter._defense, 1)
        otherCharacter._hp -= damage

    def heal(self):
        self._hp += 10
        if self._hp > 100:
            self._hp = 100
        return self._hp

    def gainExp(self, amount):
        while amount != 0:
            if self._exp + amount >= self._level * 100:
                amount -= (self._level * 100 - self._exp)
                self.levelUp()
            else:
                self._exp += amount
                amount = 0

    def levelUp(self):
        if self._level < 100:
            self._level += 1
            self._exp = 0
            self._hp += 20
            self._attackPower += 5
            self._defense += 5
        return [self._level, self._hp, self._attackPower, self._defense]

    def isAlive(self):
        return self._hp > 0

    def getName(self):
        return self._name

    def getHp(self):
        return self._hp

    def getAttackPower(self):
        return self._attackPower

    def getDefense(self):
        return self._defense

    def getLevel(self):
        return self._level

    def getExp(self):
        return self._exp