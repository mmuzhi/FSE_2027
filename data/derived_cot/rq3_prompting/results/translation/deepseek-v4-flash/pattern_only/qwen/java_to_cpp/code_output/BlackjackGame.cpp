#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <cctype>

using namespace std;

class BlackjackGame {
public:
    vector<string> deck;
    vector<string> playerHand;
    vector<string> dealerHand;

    BlackjackGame() {
        deck = createDeck();
        playerHand.clear();
        dealerHand.clear();
    }

    vector<string> createDeck() {
        vector<string> deck;
        string suits[] = {"S", "C", "D", "H"};
        string ranks[] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};

        for (const string& suit : suits) {
            for (const string& rank : ranks) {
                deck.push_back(rank + suit);
            }
        }

        random_device rd;
        mt19937 g(rd());
        shuffle(deck.begin(), deck.end(), g);

        return deck;
    }

    int calculateHandValue(const vector<string>& hand) {
        int value = 0;
        int numAces = 0;

        for (const string& card : hand) {
            string rank = card.substr(0, card.length() - 1);

            bool isNumber = !rank.empty() && all_of(rank.begin(), rank.end(), [](unsigned char c) {
                return isdigit(c);
            });

            if (isNumber) {
                value += stoi(rank);
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

    string checkWinner(const vector<string>& playerHand, const vector<string>& dealerHand) {
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
};

void printVector(const vector<string>& v) {
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i > 0) cout << ", ";
        cout << v[i];
    }
    cout << "]";
}

int main() {
    BlackjackGame game;

    printVector(game.deck);
    cout << endl;

    cout << game.calculateHandValue({"QD", "9D", "JC", "QH", "AS"}) << endl;
    cout << game.checkWinner(
        {"QD", "9D", "JC", "QH", "AS"},
        {"QD", "9D", "JC", "QH", "2S"}
    ) << endl;

    return 0;
}