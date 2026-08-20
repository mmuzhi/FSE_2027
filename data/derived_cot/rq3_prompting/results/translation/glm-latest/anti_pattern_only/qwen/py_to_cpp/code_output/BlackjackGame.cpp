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

    BlackjackGame()
        : deck(create_deck()) {
        // player_hand and dealer_hand start out empty.
    }

    // Create a deck of 52 cards (Jokers removed) in random order,
    // format is ['AS', '2S', ...].
    std::vector<std::string> create_deck() {
        std::vector<std::string> deck;
        const std::vector<std::string> suits = {"S", "C", "D", "H"};
        const std::vector<std::string> ranks = {"A", "2", "3", "4", "5", "6",
                                                "7", "8", "9", "10", "J", "Q", "K"};
        deck.reserve(52);
        for (const std::string& suit : suits) {
            for (const std::string& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        std::shuffle(deck.begin(), deck.end(), rng());
        return deck;
    }

    // Calculate the value of the poker cards stored in hand list
    // according to the rules of the Blackjack Game.
    int calculate_hand_value(const std::vector<std::string>& hand) const {
        int value = 0;
        int num_aces = 0;
        for (const std::string& card : hand) {
            // Python's card[:-1]: everything except the last character.
            const std::string rank = card.substr(0, card.size() - 1);
            if (is_digit_str(rank)) {
                value += std::stoi(rank);
            } else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            } else if (rank == "A") {
                value += 11;
                ++num_aces;
            }
        }
        while (value > 21 && num_aces > 0) {
            value -= 10;
            --num_aces;
        }
        return value;
    }

    // Determines the winner by comparing the hand values of the
    // player and dealer. Returns 'Dealer wins' or 'Player wins'.
    std::string check_winner(const std::vector<std::string>& player_hand,
                             const std::vector<std::string>& dealer_hand) const {
        const int player_value = calculate_hand_value(player_hand);
        const int dealer_value = calculate_hand_value(dealer_hand);
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
    // Persistent random engine, mirroring Python's global `random` module state.
    static std::mt19937& rng() {
        static std::mt19937 engine{std::random_device{}()};
        return engine;
    }

    // Equivalent of Python's str.isdigit(): non-empty and all digits.
    static bool is_digit_str(const std::string& s) {
        return !s.empty() && std::all_of(s.begin(), s.end(),
                                         [](unsigned char c) { return std::isdigit(c) != 0; });
    }
};