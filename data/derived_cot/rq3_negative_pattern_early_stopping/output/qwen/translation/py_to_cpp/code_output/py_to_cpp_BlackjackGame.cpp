#include <random>
#include <vector>
#include <string>

class BlackjackGame {
public:
    BlackjackGame() {
        deck = create_deck();
        player_hand = {};
        dealer_hand = {};
    }

    std::vector<std::string> create_deck() {
        std::vector<std::string> deck;
        std::vector<char> suits = {'S', 'C', 'D', 'H'};
        std::vector<std::string> ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (char suit : suits) {
            for (const std::string& rank : ranks) {
                deck.push_back(rank + std::string(1, suit));
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
        for (const std::string& card : hand) {
            char rank = card[0];
            if (rank >= '2' && rank <= '9') {
                value += (rank - '0');
            } else if (rank == '1') {
                value += 10;
            } else if (rank == 'A') {
                value += 11;
                num_aces++;
            } else { // J, Q, K
                value += 10;
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
            if (player_value <= dealer_value) return "Player wins";
            else return "Dealer wins";
        } else if (player_value > 21) {
            return "Dealer wins";
        } else if (dealer_value > 21) {
            return "Player wins";
        } else {
            if (player_value <= dealer_value) return "Dealer wins";
            else return "Player wins";
        }
    }

private:
    std::vector<std::string> deck;
    std::vector<std::string> player_hand;
    std::vector<std::string> dealer_hand;
};