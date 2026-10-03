#include <string>
#include <vector>
#include <algorithm>

class RPGCharacter {
private:
    std::string name;
    int hp;
    int attackPower;
    int defense;
    int level;
    int exp;

public:
    RPGCharacter(const std::string& name, int hp, int attackPower, int defense, int level)
        : name(name), hp(hp), attackPower(attackPower), defense(defense), level(level), exp(0) {}

    RPGCharacter(const std::string& name, int hp, int attackPower, int defense)
        : RPGCharacter(name, hp, attackPower, defense, 1) {}

    void attack(RPGCharacter& otherCharacter) {
        int damage = std::max(this->attackPower - otherCharacter.defense, 1);
        otherCharacter.hp -= damage;
    }

    int heal() {
        this->hp += 10;
        if (this->hp > 100) {
            this->hp = 100;
        }
        return this->hp;
    }

    void gainExp(int amount) {
        while (amount != 0) {
            if (this->exp + amount >= this->level * 100) {
                amount -= (this->level * 100 - this->exp);
                levelUp();
            } else {
                this->exp += amount;
                amount = 0;
            }
        }
    }

    std::vector<int> levelUp() {
        if (this->level < 100) {
            this->level += 1;
            this->exp = 0;
            this->hp += 20;
            this->attackPower += 5;
            this->defense += 5;
        }
        return {this->level, this->hp, this->attackPower, this->defense};
    }

    bool isAlive() const {
        return this->hp > 0;
    }

    // Getters
    std::string getName() const { return name; }
    int getHp() const { return hp; }
    int getAttackPower() const { return attackPower; }
    int getDefense() const { return defense; }
    int getLevel() const { return level; }
    int getExp() const { return exp; }
};