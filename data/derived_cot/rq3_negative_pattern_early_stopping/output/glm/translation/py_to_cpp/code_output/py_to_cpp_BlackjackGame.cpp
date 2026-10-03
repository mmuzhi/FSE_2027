#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <cctype>

class BlackjackGame {
private:
    std::vector<std::string> deck;
    std::vector<std::string> player_hand;
    std::vector<std::string> dealer_hand;

public:
    BlackjackGame() : deck(create_deck()) {}

    std::vector<std::string> create_deck() {
        std::vector<std::string> deck;
        std::vector<std::string> suits = {"S", "C", "D", "H"};
        std::vector<std::string> ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        
        for (const auto& suit : suits) {
            for (const auto& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(deck.begin(), deck.end(), g);
        
        return deck;
    }

    int calculate_hand_value(const std::vector<std::string>& hand) {
        int value = 0;
        int num_aces = 0;
        
        for (const auto& card : hand) {
            std::string rank = card.substr(0, card.size() - 1);
            if (std::isdigit(static_cast<unsigned char>(rank[0]))) {
                value += std::stoi(rank);
            } else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            } else if (rank == "A") {
                value += 11;
                num_aces++;
            }
        }
        
        while (value > 21 && num_aces > 0) {
            value -= 10;
            num_aces--;
        }
        
        return value;
    }

    std::string check_winner(const std::vector<std::string>& player_hand, const std::vector<std::string>& dealer_hand) {
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
};