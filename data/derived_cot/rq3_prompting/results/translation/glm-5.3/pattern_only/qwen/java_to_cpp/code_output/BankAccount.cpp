#include <iostream>
#include <stdexcept>

class BankAccount {
private:
    int balance;

public:
    explicit BankAccount(int balance) : balance(balance) {}

    BankAccount() : BankAccount(0) {}

    int deposit(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        this->balance += amount;
        return this->balance;
    }

    int withdraw(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        if (amount > this->balance) {
            throw std::invalid_argument("Insufficient balance.");
        }
        this->balance -= amount;
        return this->balance;
    }

    int viewBalance() {
        return this->balance;
    }

    void transfer(BankAccount& otherAccount, int amount) {
        this->withdraw(amount);
        otherAccount.deposit(amount);
    }
};

int main() {
    BankAccount account1;
    BankAccount account2;
    account1.deposit(1000);
    account1.transfer(account2, 300);
    std::cout << "account1.balance = " << account1.viewBalance() << "\n";
    std::cout << "account2.balance = " << account2.viewBalance() << "\n";
    return 0;
}