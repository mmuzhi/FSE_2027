#include <string>
#include <tuple>
#include <algorithm>
#include <utility>

class RPGCharacter {
public:
    std::string name;
    int hp;
    int attack_power;
    int defense;
    int level;
    int exp;

    RPGCharacter(std::string name, int hp, int attack_power, int defense, int level = 1)
        : name(std::move(name)), hp(hp), attack_power(attack_power), defense(defense), level(level), exp(0) {}

    void attack(RPGCharacter& other_character) {
        int damage = std::max(this->attack_power - other_character.defense, 1);
        other_character.hp -= damage;
    }

    int heal() {
        this->hp += 10;
        if (this->hp > 100) {
            this->hp = 100;
        }
        return this->hp;
    }

    void gain_exp(int amount) {
        while (amount != 0) {
            if (this->exp + amount >= this->level * 100) {
                amount -= (this->level * 100 - this->exp);
                this->level_up();
            } else {
                this->exp += amount;
                amount = 0;
            }
        }
    }

    std::tuple<int, int, int, int> level_up() {
        if (this->level < 100) {
            this->level += 1;
            this->exp = 0;
            this->hp += 20;
            this->attack_power += 5;
            this->defense += 5;
        }
        return std::make_tuple(this->level, this->hp, this->attack_power, this->defense);
    }

    bool is_alive() {
        return this->hp > 0;
    }
};