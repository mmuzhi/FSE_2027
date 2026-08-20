class BankAccount:
    def __init__(self, balance: int = 0):
        self._balance = balance

    def deposit(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Invalid amount")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Invalid amount")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        return self._balance

    def viewBalance(self) -> int:
        return self._balance

    def transfer(self, other_account: "BankAccount", amount: int) -> None:
        self.withdraw(amount)
        other_account.deposit(amount)


if __name__ == "__main__":
    account1 = BankAccount()
    account2 = BankAccount()
    account1.deposit(1000)
    account1.transfer(account2, 300)
    print("account1.balance = " + str(account1.viewBalance()))
    print("account2.balance = " + str(account2.viewBalance()))