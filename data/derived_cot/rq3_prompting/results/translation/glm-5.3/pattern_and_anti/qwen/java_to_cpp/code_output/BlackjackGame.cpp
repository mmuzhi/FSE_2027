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

    // Replicates Java's List.toString() format: [a, b, c]
    static std::string javaListToString(const std::vector<std::string>& list) {
        std::string result = "[";
        for (std::size_t i = 0; i < list.size(); ++i) {
            if (i > 0) result += ", ";
            result += list[i];
        }
        result += "]";
        return result;
    }

public:
    BlackjackGame()
        : deck(createDeck()), playerHand(), dealerHand() {}

    std::vector<std::string> createDeck() const {
        std::vector<std::string> newDeck;
        const char* suits[] = {"S", "C", "D", "H"};
        const char* ranks[] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (const char* suit : suits) {
            for (const char* rank : ranks) {
                newDeck.push_back(std::string(rank) + suit);
            }
        }
        std::shuffle(newDeck.begin(), newDeck.end(),
                     std::mt19937(std::random_device{}()));
        return newDeck;
    }

    int calculateHandValue(const std::vector<std::string>& hand) const {
        int value = 0;
        int numAces = 0;
        for (const std::string& card : hand) {
            std::string rank = card.substr(0, card.length() - 1);
            bool allDigits = !rank.empty() && std::all_of(rank.begin(), rank.end(),
                [](unsigned char c) { return std::isdigit(c) != 0; });
            if (allDigits) {
                value += std::stoi(rank);
            }
            else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            }
            else if (rank == "A") {
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

    std::string checkWinner(const std::vector<std::string>& playerHand,
                            const std::vector<std::string>& dealerHand) const {
        int playerValue = calculateHandValue(playerHand);
        int dealerValue = calculateHandValue(dealerHand);
        if (playerValue > 21 && dealerValue > 21) {
            return playerValue <= dealerValue ? "Player wins" : "Dealer wins";
        }
        else if (playerValue > 21) {
            return "Dealer wins";
        }
        else if (dealerValue > 21) {
            return "Player wins";
        }
        else {
            return playerValue > dealerValue ? "Player wins" : "Dealer wins";
        }
    }

    static void main() {
        BlackjackGame game;
        std::cout << javaListToString(game.deck) << std::endl;
        std::cout << game.calculateHandValue({"QD", "9D", "JC", "QH", "AS"}) << std::endl;
        std::cout << game.checkWinner({"QD", "9D", "JC", "QH", "AS"},
                                      {"QD", "9D", "JC", "QH", "2S"}) << std::endl;
    }
};

int main() {
    BlackjackGame::main();
    return 0;
}