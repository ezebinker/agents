import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(user_id='12345', name='John Doe', initial_deposit=1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.current_balance(), 1500.0)

    def test_withdraw(self):
        initial_balance = self.account.current_balance()
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.current_balance(), initial_balance - 200.0)

    def test_withdraw_insufficient_funds(self):
        initial_balance = self.account.current_balance()
        result = self.account.withdraw(2000.0)
        self.assertFalse(result)
        self.assertEqual(self.account.current_balance(), initial_balance)

    def test_buy_shares(self):
        initial_balance = self.account.current_balance()
        result = self.account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.current_balance(), initial_balance - get_share_price('AAPL') * 5)
        self.assertEqual(self.account.get_holdings().get('AAPL', 0), 5)

    def test_buy_shares_insufficient_funds(self):
        result = self.account.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.get_holdings().get('GOOGL', 0), 0)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 5)
        initial_balance = self.account.current_balance()
        result = self.account.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.current_balance(), initial_balance + get_share_price('AAPL') * 3)
        self.assertEqual(self.account.get_holdings().get('AAPL', 0), 2)

    def test_sell_shares_insufficient_quantity(self):
        self.account.buy_shares('AAPL', 2)
        result = self.account.sell_shares('AAPL', 3)
        self.assertFalse(result)
        self.assertEqual(self.account.get_holdings().get('AAPL', 0), 2)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        expected_value = get_share_price('AAPL') * 2 + get_share_price('TSLA')
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)

    def test_calculate_profit_loss(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 5)
        expected_profit_loss = self.account.calculate_portfolio_value() + self.account.current_balance() - 1000.0
        self.assertEqual(self.account.calculate_profit_loss(), expected_profit_loss)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 3})

    def test_get_transactions(self):
        self.account.deposit(200.0)
        self.account.withdraw(100.0)
        self.account.buy_shares('AAPL', 2)
        transactions = self.account.get_transactions()
        expected_transactions = [
            {'type': 'deposit', 'amount': 200.0},
            {'type': 'withdraw', 'amount': 100.0},
            {'type': 'buy', 'symbol': 'AAPL', 'quantity': 2}
        ]
        self.assertEqual(transactions, expected_transactions)

if __name__ == '__main__':
    unittest.main()