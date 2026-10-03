class RPGCharacter:
    def __init__(self, name: str, hp: int, attackPower: int, defense: int, level: int = 1):
        self.name = name
        self.hp = hp
        self.attackPower = attackPower
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, otherCharacter: 'RPGCharacter') -> None:
        damage = max(self.attackPower - otherCharacter.defense, 1)
        otherCharacter.hp -= damage

    def heal(self) -> int:
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def gainExp(self, amount: int) -> None:
        while amount != 0:
            if self.exp + amount >= self.level * 100:
                amount -= (self.level * 100 - self.exp)
                self.levelUp()
            else:
                self.exp += amount
                amount = 0

    def levelUp(self) -> list:
        if self.level < 100:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attackPower += 5
            self.defense += 5
        return [self.level, self.hp, self.attackPower, self.defense]

    def isAlive(self) -> bool:
        return self.hp > 0

    def getName(self) -> str:
        return self.name

    def getHp(self) -> int:
        return self.hp

    def getAttackPower(self) -> int:
        return self.attackPower

    def getDefense(self) -> int:
        return self.defense

    def getLevel(self) -> int:
        return self.level

    def getExp(self) -> int:
        return self.exp