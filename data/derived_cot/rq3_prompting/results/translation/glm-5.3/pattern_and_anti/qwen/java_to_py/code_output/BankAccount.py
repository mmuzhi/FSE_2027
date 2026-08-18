class BankAccount:
    def __init__(self, balance: int = 0):
        self.balance = balance

    def deposit(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Invalid amount")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Invalid amount")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        return self.balance

    def view_balance(self) -> int:
        return self.balance

    def transfer(self, other_account: "BankAccount", amount: int) -> None:
        self.withdraw(amount)
        other_account.deposit(amount)


def main() -> None:
    account1 = BankAccount()
    account2 = BankAccount()
    account1.deposit(1000)
    account1.transfer(account2, 300)
    print(f"account1.balance = {account1.view_balance()}")
    print(f"account2.balance = {account2.view_balance()}")


if __name__ == "__main__":
    main()