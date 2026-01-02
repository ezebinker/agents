import gradio as gr
from accounts import Account, get_share_price

# Initialize account for demonstration
account = Account(user_id='12345', name='John Doe', initial_deposit=1000.0)

def create_account(initial_deposit: float):
    global account
    account = Account(user_id='12345', name='John Doe', initial_deposit=initial_deposit)
    return f"Account created with initial deposit: ${initial_deposit}"

def deposit_funds(amount: float):
    account.deposit(amount)
    return f"Deposited ${amount}. Current Balance: ${account.current_balance()}"

def withdraw_funds(amount: float):
    if account.withdraw(amount):
        return f"Withdrew ${amount}. Current Balance: ${account.current_balance()}"
    else:
        return "Withdrawal failed. Insufficient funds."

def buy_shares(symbol: str, quantity: int):
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}. Current Balance: ${account.current_balance()}"
    else:
        return "Purchase failed. Insufficient funds or incorrect symbol."

def sell_shares(symbol: str, quantity: int):
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}. Current Balance: ${account.current_balance()}"
    else:
        return "Sale failed. Insufficient shares."

def report_portfolio():
    holdings = account.get_holdings()
    portfolio_value = account.calculate_portfolio_value()
    return f"Holdings: {holdings}, Portfolio Value: ${portfolio_value}"

def report_profit_loss():
    profit_loss = account.calculate_profit_loss()
    return f"Profit/Loss: ${profit_loss}"

def list_transactions():
    transactions = account.get_transactions()
    return f"Transactions: {transactions}"

# Create Gradio interface using Blocks for multiple functions
with gr.Blocks() as interface:
    gr.Markdown("# Account Management System")
    
    with gr.Tab("Create Account"):
        initial_deposit_input = gr.Number(label="Initial Deposit", value=1000)
        create_output = gr.Textbox(label="Output")
        create_btn = gr.Button("Create Account")
        create_btn.click(create_account, inputs=initial_deposit_input, outputs=create_output)
    
    with gr.Tab("Deposit"):
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_output = gr.Textbox(label="Output")
        deposit_btn = gr.Button("Deposit")
        deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
    
    with gr.Tab("Withdraw"):
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_output = gr.Textbox(label="Output")
        withdraw_btn = gr.Button("Withdraw")
        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Buy Shares"):
        buy_symbol = gr.Textbox(label="Buy Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Number(label="Buy Quantity")
        buy_output = gr.Textbox(label="Output")
        buy_btn = gr.Button("Buy Shares")
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
    
    with gr.Tab("Sell Shares"):
        sell_symbol = gr.Textbox(label="Sell Symbol (AAPL, TSLA, GOOGL)")
        sell_quantity = gr.Number(label="Sell Quantity")
        sell_output = gr.Textbox(label="Output")
        sell_btn = gr.Button("Sell Shares")
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        portfolio_output = gr.Textbox(label="Portfolio Report")
        portfolio_btn = gr.Button("Get Portfolio Report")
        portfolio_btn.click(report_portfolio, inputs=None, outputs=portfolio_output)
    
    with gr.Tab("Profit/Loss"):
        profit_loss_output = gr.Textbox(label="Profit/Loss Report")
        profit_loss_btn = gr.Button("Get Profit/Loss Report")
        profit_loss_btn.click(report_profit_loss, inputs=None, outputs=profit_loss_output)
    
    with gr.Tab("Transactions"):
        transactions_output = gr.Textbox(label="Transaction History")
        transactions_btn = gr.Button("Get Transactions")
        transactions_btn.click(list_transactions, inputs=None, outputs=transactions_output)

# Launch the interface
if __name__ == "__main__":
    interface.launch()