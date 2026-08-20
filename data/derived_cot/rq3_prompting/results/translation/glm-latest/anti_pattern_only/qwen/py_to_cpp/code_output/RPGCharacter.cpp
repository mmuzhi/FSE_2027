#include <string>
#include <algorithm>
#include <tuple>

// The class represents a role-playing game character, which allows to attack
// other characters, heal, gain experience, level up, and check if the
// character is alive.
class RPGCharacter {
public:
    std::string name;
    int hp;
    int attack_power;
    int defense;
    int level;
    int exp;

    // Initialize an RPG character object.
    // :param name: the name of the character.
    // :param hp: The health points of the character.
    // :param attack_power: the attack power of the character.
    // :param defense: the defense points of the character.
    // :param level: the level of the character. Default is 1.
    RPGCharacter(std::string name, int hp, int attack_power, int defense, int level = 1)
        : name(std::move(name)), hp(hp), attack_power(attack_power),
          defense(defense), level(level), exp(0) {}

    // Attack another character. The damage caused needs to offset the defense value.
    void attack(RPGCharacter& other_character) {
        int damage = std::max(attack_power - other_character.defense, 1);
        other_character.hp -= damage;
    }

    // Heal the character with 10 hp and the max hp is 100.
    // :return: the current health points after healing.
    int heal() {
        hp += 10;
        if (hp > 100) {
            hp = 100;
        }
        return hp;
    }

    // Gain experience points for the character and level up when the exp has
    // reached the value that is 100 times the current level.
    // The experience that overflows should be used to calculate the next
    // level up until exhausted.
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

    // Level up the character and return to zero experience points, increase
    // hp by 20 points, attack power and defense points by 5 points.
    // Max level is 100.
    // :return: tuple of (level, hp, attack_power, defense) after leveling up.
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

    // Check if the player is alive.
    // :return: true if the hp is larger than 0, or false otherwise.
    bool is_alive() const {
        return hp > 0;
    }
};