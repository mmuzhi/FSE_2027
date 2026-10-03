#include <string>
#include <tuple>
#include <algorithm> // for std::max

class RPGCharacter {
private:
    std::string name;
    int hp;
    int attack_power;
    int defense;
    int level;
    int exp;

public:
    // Constructor
    RPGCharacter(const std::string& name, int hp, int attack_power, int defense, int level = 1)
        : name(name), hp(hp), attack_power(attack_power), defense(defense), level(level), exp(0) {}

    // Attack method
    void attack(RPGCharacter& other_character) {
        int damage = std::max(this->attack_power - other_character.defense, 1);
        other_character.hp -= damage;
    }

    // Heal method
    int heal() {
        this->hp += 10;
        if (this->hp > 100) {
            this->hp = 100;
        }
        return this->hp;
    }

    // Gain experience
    void gain_exp(int amount) {
        while (amount != 0) {
            if (this->exp + amount >= this->level * 100) {
                int needed_exp = this->level * 100 - this->exp;
                amount -= needed_exp;
                this->level_up();
            } else {
                this->exp += amount;
                amount = 0;
            }
        }
    }

    // Level up method
    std::tuple<int, int, int, int> level_up() {
        if (this->level < 100) {
            this->level++;
            this->exp = 0;
            this->hp += 20;
            this->attack_power += 5;
            this->defense += 5;
        }
        return std::make_tuple(this->level, this->hp, this->attack_power, this->defense);
    }

    // Check if alive
    bool is_alive() const {
        return this->hp > 0;
    }
};