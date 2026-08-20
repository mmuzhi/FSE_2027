#include <iostream>
#include <stdexcept>

class BankAccount {
private:
    int balance;

public:
    explicit BankAccount(int balance) : balance(balance) {}

    // Mirrors Java's `this(0)` default constructor.
    BankAccount() : BankAccount(0) {}

    int deposit(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        // Java's int arithmetic wraps on overflow; unsigned math reproduces
        // that exactly instead of invoking UB.
        this->balance = static_cast<int>(static_cast<unsigned int>(this->balance) +
                                         static_cast<unsigned int>(amount));
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

    int viewBalance() const {
        return this->balance;
    }

    // Java passes object references; BankAccount& is the C++ equivalent.
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
    std::cout << "account1.balance = " << account1.viewBalance() << std::endl;
    std::cout << "account2.balance = " << account2.viewBalance() << std::endl;
    return 0;
}