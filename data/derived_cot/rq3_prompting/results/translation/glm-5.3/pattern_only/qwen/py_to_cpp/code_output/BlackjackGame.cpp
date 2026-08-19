#include <algorithm>
#include <cctype>
#include <random>
#include <string>
#include <vector>

class BlackjackGame {
public:
    std::vector<std::string> deck;
    std::vector<std::string> player_hand;
    std::vector<std::string> dealer_hand;

    BlackjackGame() : deck(create_deck()) {}

    std::vector<std::string> create_deck() {
        std::vector<std::string> deck;
        std::vector<std::string> suits = {"S", "C", "D", "H"};
        std::vector<std::string> ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (const std::string& suit : suits) {
            for (const std::string& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        std::shuffle(deck.begin(), deck.end(), rng());
        return deck;
    }

    int calculate_hand_value(const std::vector<std::string>& hand) {
        int value = 0;
        int num_aces = 0;
        for (const std::string& card : hand) {
            std::string rank = card.substr(0, card.size() - 1);
            if (is_digits(rank)) {
                value += std::stoi(rank);
            } else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            } else if (rank == "A") {
                value += 11;
                num_aces += 1;
            }
        }
        while (value > 21 && num_aces > 0) {
            value -= 10;
            num_aces -= 1;
        }
        return value;
    }

    std::string check_winner(const std::vector<std::string>& player_hand,
                             const std::vector<std::string>& dealer_hand) {
        int player_value = calculate_hand_value(player_hand);
        int dealer_value = calculate_hand_value(dealer_hand);
        if (player_value > 21 && dealer_value > 21) {
            if (player_value <= dealer_value) {
                return "Player wins";
            } else {
                return "Dealer wins";
            }
        } else if (player_value > 21) {
            return "Dealer wins";
        } else if (dealer_value > 21) {
            return "Player wins";
        } else {
            if (player_value <= dealer_value) {
                return "Dealer wins";
            } else {
                return "Player wins";
            }
        }
    }

private:
    static std::mt19937& rng() {
        static std::mt19937 engine(std::random_device{}());
        return engine;
    }

    static bool is_digits(const std::string& s) {
        if (s.empty()) return false;
        for (char c : s) {
            if (!std::isdigit(static_cast<unsigned char>(c))) {
                return false;
            }
        }
        return true;
    }
};