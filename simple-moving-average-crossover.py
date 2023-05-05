import backtrader as bt
import yfinance as yf

#Define the variables
per = 5
initial_cash = 100000

# Define the strategy
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=per)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

# Download data from Yahoo Finance
data = yf.download('SPY', start='2017-01-01', end='2022-01-01')

# Create a Backtrader feed from the Yahoo Finance data
data_feed = bt.feeds.PandasData(dataname=data)

# Initialize a Backtrader cerebro instance
cerebro = bt.Cerebro()

# Add the data feed to cerebro
cerebro.adddata(data_feed)

# Add the strategy to cerebro
cerebro.addstrategy(MyStrategy)

# Set the initial cash balance of the portfolio to $100,000
cerebro.broker.setcash(initial_cash)

# Set the commission for buying and selling assets to 0.1%
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
cerebro.run()
cerebro.plot()

# Print the final portfolio value
print('Final portfolio value: ${}'.format(cerebro.broker.getvalue()))
gain = round(cerebro.broker.getvalue() - initial_cash, 2)
gain_percent = round(((cerebro.broker.getvalue() - initial_cash)/initial_cash)*100, 2)
print('Gain: ${}'.format(gain), ",", "%d%%"%gain_percent)
