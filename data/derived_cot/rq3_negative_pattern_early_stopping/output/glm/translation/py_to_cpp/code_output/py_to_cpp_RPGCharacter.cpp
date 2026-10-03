#include <string>
#include <algorithm>
#include <tuple>

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
        int damage = std::max(attack_power - other_character.defense, 1);
        other_character.hp -= damage;
    }

    int heal() {
        hp += 10;
        if (hp > 100) {
            hp = 100;
        }
        return hp;
    }

    void gain_exp(int amount) {
        while (amount != 0) {
            if (exp + amount >= level * 100) {
                amount -= (level * 100 - exp);
                level_up();
            } else {
                exp += amount;
                amount = 0;
            }
        }
    }

    std::tuple<int, int, int, int> level_up() {
        if (level < 100) {
            level += 1;
            exp = 0;
            hp += 20;
            attack_power += 5;
            defense += 5;
        }
        return std::make_tuple(level, hp, attack_power, defense);
    }

    bool is_alive() {
        return hp > 0;
    }
};