#include <algorithm>
#include <cctype>
#include <iostream>
#include <random>
#include <string>
#include <vector>

class BlackjackGame {
private:
    std::vector<std::string> deck;
    std::vector<std::string> playerHand;
    std::vector<std::string> dealerHand;

    static bool isAllDigits(const std::string& s) {
        if (s.empty()) return false;
        for (char c : s) {
            if (!std::isdigit(static_cast<unsigned char>(c))) return false;
        }
        return true;
    }

public:
    BlackjackGame()
        : deck(createDeck()), playerHand(), dealerHand() {}

    std::vector<std::string> createDeck() {
        std::vector<std::string> deck;
        const std::string suits[] = {"S", "C", "D", "H"};
        const std::string ranks[] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (const std::string& suit : suits) {
            for (const std::string& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        std::shuffle(deck.begin(), deck.end(), std::mt19937(std::random_device{}()));
        return deck;
    }

    int calculateHandValue(const std::vector<std::string>& hand) {
        int value = 0;
        int numAces = 0;
        for (const std::string& card : hand) {
            std::string rank = card.substr(0, card.length() - 1);
            if (isAllDigits(rank)) {
                value += std::stoi(rank);
            } else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            } else if (rank == "A") {
                value += 11;
                numAces += 1;
            }
        }
        while (value > 21 && numAces > 0) {
            value -= 10;
            numAces -= 1;
        }
        return value;
    }

    std::string checkWinner(const std::vector<std::string>& playerHand, const std::vector<std::string>& dealerHand) {
        int playerValue = calculateHandValue(playerHand);
        int dealerValue = calculateHandValue(dealerHand);
        if (playerValue > 21 && dealerValue > 21) {
            return playerValue <= dealerValue ? "Player wins" : "Dealer wins";
        } else if (playerValue > 21) {
            return "Dealer wins";
        } else if (dealerValue > 21) {
            return "Player wins";
        } else {
            return playerValue > dealerValue ? "Player wins" : "Dealer wins";
        }
    }

    friend int main();
};

int main() {
    BlackjackGame game;
    // Mimics Java's List.toString() format: [elem, elem, ...]
    std::cout << '[';
    for (std::size_t i = 0; i < game.deck.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << game.deck[i];
    }
    std::cout << ']' << std::endl;
    std::cout << game.calculateHandValue({"QD", "9D", "JC", "QH", "AS"}) << std::endl;
    std::cout << game.checkWinner({"QD", "9D", "JC", "QH", "AS"}, {"QD", "9D", "JC", "QH", "2S"}) << std::endl;
    return 0;
}