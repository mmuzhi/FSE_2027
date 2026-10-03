class BankAccount:
    def __init__(self, balance=0.0):
        self._balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Invalid amount")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Invalid amount")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        return self._balance

    def view_balance(self):
        return self._balance

    def transfer(self, other_account, amount):
        self.withdraw(amount)
        other_account.deposit(amount)