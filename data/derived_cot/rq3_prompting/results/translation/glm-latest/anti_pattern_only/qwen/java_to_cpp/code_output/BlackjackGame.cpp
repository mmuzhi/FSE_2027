#include <algorithm>
#include <cctype>
#include <iostream>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace org::example {

class BlackjackGame {
private:
    std::vector<std::string> deck;
    std::vector<std::string> playerHand;
    std::vector<std::string> dealerHand;

public:
    BlackjackGame()
        : deck(createDeck()),
          playerHand(),
          dealerHand() {}

    std::vector<std::string> createDeck() {
        std::vector<std::string> deck;
        const std::string suits[] = {"S", "C", "D", "H"};
        const std::string ranks[] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (const std::string& suit : suits) {
            for (const std::string& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        // Java: Collections.shuffle(deck, new Random()) — unseeded, random per run.
        std::mt19937 rng(std::random_device{}());
        std::shuffle(deck.begin(), deck.end(), rng);
        return deck;
    }

    int calculateHandValue(const std::vector<std::string>& hand) const {
        int value = 0;
        int numAces = 0;
        for (const std::string& card : hand) {
            if (card.empty()) {
                // Java: card.substring(0, card.length() - 1) throws StringIndexOutOfBoundsException.
                throw std::out_of_range("String index out of range: -1");
            }
            const std::string rank = card.substr(0, card.length() - 1);
            const bool numeric = !rank.empty() && std::all_of(
                rank.begin(), rank.end(),
                [](unsigned char c) { return std::isdigit(c) != 0; });
            if (numeric) {
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

    std::string checkWinner(const std::vector<std::string>& playerHand,
                            const std::vector<std::string>& dealerHand) const {
        const int playerValue = calculateHandValue(playerHand);
        const int dealerValue = calculateHandValue(dealerHand);
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

    static int main() {
        BlackjackGame game;
        std::cout << toJavaListString(game.deck) << '\n';
        std::cout << game.calculateHandValue({"QD", "9D", "JC", "QH", "AS"}) << '\n';
        std::cout << game.checkWinner({"QD", "9D", "JC", "QH", "AS"},
                                      {"QD", "9D", "JC", "QH", "2S"}) << '\n';
        return 0;
    }

private:
    // Formats like Java's List.toString(): "[a, b, c]"
    static std::string toJavaListString(const std::vector<std::string>& list) {
        std::ostringstream out;
        out << '[';
        for (std::size_t i = 0; i < list.size(); ++i) {
            if (i > 0) out << ", ";
            out << list[i];
        }
        out << ']';
        return out.str();
    }
};

} // namespace org::example

int main() {
    return org::example::BlackjackGame::main();
}