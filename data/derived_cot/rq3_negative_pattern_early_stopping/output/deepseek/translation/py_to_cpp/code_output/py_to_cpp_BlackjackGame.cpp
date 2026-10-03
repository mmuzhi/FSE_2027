#include <algorithm>
#include <random>
#include <string>
#include <vector>

class BlackjackGame {
public:
    // Constructor: creates a shuffled deck and initializes empty hands
    BlackjackGame() : deck(create_deck()), player_hand(), dealer_hand() {}

    // Creates a deck of 52 cards (suits: S, C, D, H; ranks: A,2-10,J,Q,K) and shuffles it
    std::vector<std::string> create_deck() {
        std::vector<std::string> deck;
        std::string suits = "SCDH";
        std::string ranks = "A2345678910JQK"; // note: '10' is represented as two characters, but we need to handle separately
        // Actually we need to include "10" properly; we'll store ranks separately or handle as special case.
        // For simplicity, we'll iterate over the actual rank strings.
        std::vector<std::string> rank_strings = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (char suit : suits) {
            for (const std::string& rank : rank_strings) {
                deck.push_back(rank + suit);
            }
        }
        // Shuffle deck using a cryptographically random seed
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(deck.begin(), deck.end(), g);
        return deck;
    }

    // Calculates the total value of a hand according to blackjack rules.
    // Aces are initially counted as 11, but reduced to 1 if the hand would bust.
    int calculate_hand_value(const std::vector<std::string>& hand) const {
        int value = 0;
        int num_aces = 0;
        for (const std::string& card : hand) {
            // Extract rank (everything except the last character, which is the suit)
            std::string rank = card.substr(0, card.size() - 1);
            if (rank == "A") {
                value += 11;
                ++num_aces;
            } else if (rank == "J" || rank == "Q" || rank == "K" || rank == "10") {
                value += 10;
            } else {
                // rank is a digit from "2" to "9"
                value += std::stoi(rank);
            }
        }
        // Convert aces from 11 to 1 as long as the hand busts
        while (value > 21 && num_aces > 0) {
            value -= 10;
            --num_aces;
        }
        return value;
    }

    // Determines the winner by comparing hand values.
    // Returns "Player wins" or "Dealer wins" exactly as in the Python implementation.
    std::string check_winner(const std::vector<std::string>& player_hand,
                             const std::vector<std::string>& dealer_hand) const {
        int player_value = calculate_hand_value(player_hand);
        int dealer_value = calculate_hand_value(dealer_hand);

        if (player_value > 21 && dealer_value > 21) {
            return (player_value <= dealer_value) ? "Player wins" : "Dealer wins";
        } else if (player_value > 21) {
            return "Dealer wins";
        } else if (dealer_value > 21) {
            return "Player wins";
        } else {
            return (player_value <= dealer_value) ? "Dealer wins" : "Player wins";
        }
    }

private:
    std::vector<std::string> deck;
    std::vector<std::string> player_hand;
    std::vector<std::string> dealer_hand;
};