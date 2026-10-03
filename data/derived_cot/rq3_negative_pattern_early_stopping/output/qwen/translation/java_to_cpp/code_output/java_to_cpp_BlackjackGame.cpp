#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <cctype>
#include <random>

using namespace std;

class BlackjackGame {
private:
    vector<string> deck;
    vector<string> playerHand;
    vector<string> dealerHand;

    vector<string> createDeck() {
        vector<string> deck;
        string suits[] = {"S", "C", "D", "H"};
        string ranks[] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        for (char suit : suits) {
            for (string rank : ranks) {
                deck.push_back(rank + suit);
            }
        }
        shuffle(deck.begin(), deck.end(), random_device());
        return deck;
    }

    int calculateHandValue(const vector<string>& hand) {
        int value = 0;
        int numAces = 0;
        for (const string& card : hand) {
            string rank = card.substr(0, card.size() - 1);
            if (isdigit(rank[0])) {
                value += stoi(rank);
            }
            else if (rank == "J" || rank == "Q" || rank == "K") {
                value += 10;
            }
            else if (rank == "A") {
                value += 11;
                numAces++;
            }
        }
        while (value > 21 && numAces > 0) {
            value -= 10;
            numAces--;
        }
        return value;
    }

public:
    BlackjackGame() : deck(createDeck()), playerHand(), dealerHand() {}

    string checkWinner(const vector<string>& playerHand, const vector<string>& dealerHand) {
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

    static void printDeck() {
        BlackjackGame game;
        for (const string& card : game.deck) {
            cout << card << " ";
        }
        cout << endl;
    }
};

int main() {
    BlackjackGame game;
    game.printDeck();
    cout << game.calculateHandValue({"QD", "9D", "JC", "QH", "AS"}) << endl;
    cout << game.checkWinner({"QD", "9D", "JC", "QH", "AS"}, {"QD", "9D", "JC", "QH", "2S"}) << endl;
    return 0;
}