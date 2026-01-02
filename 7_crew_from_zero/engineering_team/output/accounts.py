class Account:
    def __init__(self, user_id: str, name: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.name = name
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append({'type': 'withdraw', 'amount': amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
            self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity})
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if self.portfolio.get(symbol, 0) >= quantity:
            share_price = get_share_price(symbol)
            total_gain = share_price * quantity
            self.balance += total_gain
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity})
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() + self.balance - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio.copy()

    def get_transactions(self) -> list:
        return self.transactions.copy()

    def current_balance(self) -> float:
        return self.balance


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 600.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

# Sample usage
account = Account(user_id='12345', name='John Doe', initial_deposit=1000.0)
account.deposit(500.0)
account.withdraw(300.0)
account.buy_shares('AAPL', 5)
account.sell_shares('AAPL', 2)
portfolio_value = account.calculate_portfolio_value()
profit_loss = account.calculate_profit_loss()
holdings = account.get_holdings()
transactions = account.get_transactions()
balance = account.current_balance()

print('Portfolio Value:', portfolio_value)
print('Profit/Loss:', profit_loss)
print('Holdings:', holdings)
print('Transactions:', transactions)
print('Balance:', balance)