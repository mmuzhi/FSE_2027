class RPGCharacter:
    def __init__(self, name, hp, attackPower, defense, level=1):
        self.name = name
        self.hp = hp
        self.attackPower = attackPower
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other_character):
        damage = max(self.attackPower - other_character.defense, 1)
        other_character.hp -= damage

    def heal(self):
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def gain_exp(self, amount):
        while amount != 0:
            if self.exp + amount >= self.level * 100:
                to_add = self.level * 100 - self.exp
                self.exp += to_add
                amount -= to_add
                self.level_up()
            else:
                self.exp += amount
                amount = 0

    def level_up(self):
        if self.level < 100:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attackPower += 5
            self.defense += 5
        return (self.level, self.hp, self.attackPower, self.defense)

    def is_alive(self):
        return self.hp > 0

    # Getters
    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_attack_power(self):
        return self.attackPower

    def get_defense(self):
        return self.defense

    def get_level(self):
        return self.level

    def get_exp(self):
        return self.exp