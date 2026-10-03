class RPGCharacter:
    def __init__(self, name: str, hp: int, attack_power: int, defense: int, level: int = 1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other_character: 'RPGCharacter') -> None:
        damage = max(self.attack_power - other_character.defense, 1)
        other_character.hp -= damage

    def heal(self) -> int:
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def gain_exp(self, amount: int) -> None:
        while amount != 0:
            if self.exp + amount >= self.level * 100:
                amount -= (self.level * 100 - self.exp)
                self.level_up()
            else:
                self.exp += amount
                amount = 0

    def level_up(self) -> None:
        if self.level < 100:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attack_power += 5
            self.defense += 5

    def is_alive(self) -> bool:
        return self.hp > 0

    def get_hp(self) -> int:
        return self.hp

    def get_exp(self) -> int:
        return self.exp

    def get_attack_power(self) -> int:
        return self.attack_power

    def get_defense(self) -> int:
        return self.defense

    def get_level(self) -> int:
        return self.level

    def set_hp(self, x: int) -> None:
        self.hp = x