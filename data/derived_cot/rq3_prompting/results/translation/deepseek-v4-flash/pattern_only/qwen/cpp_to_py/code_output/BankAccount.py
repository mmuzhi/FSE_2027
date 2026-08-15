class InvalidArgument(ValueError):
    pass


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise InvalidArgument("Invalid amount")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            raise InvalidArgument("Invalid amount")
        if amount > self.balance:
            raise InvalidArgument("Insufficient balance.")
        self.balance -= amount
        return self.balance

    def view_balance(self):
        return self.balance

    def transfer(self, otherAccount, amount):
        self.withdraw(amount)
        otherAccount.deposit(amount)