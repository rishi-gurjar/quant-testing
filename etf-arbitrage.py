import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

class QCLNStrategy(bt.Strategy):
    def __init__(self):
        self.qcln = self.datas[0]
        self.qcln2 = self.datas[1]
        self.spread = self.qcln - self.qcln2
        self.arbitrage_opportunities = []

    def next(self):
        if self.spread[0] > 2.0:  # arbitrage opportunity
            size = min(self.broker.getcash() // self.qcln2[0], self.broker.getposition(self.qcln).size)
            self.buy(self.qcln2, size=size)
            self.sell(self.qcln, size=size)
            self.arbitrage_opportunities.append((self.data.datetime.datetime(0), 'Buy QCLN2, Sell QCLN', size, self.spread[0]))
        elif self.spread[0] < -2.0:
            size = min(self.broker.getcash() // self.qcln[0], self.broker.getposition(self.qcln2).size)
            self.buy(self.qcln, size=size)
            self.sell(self.qcln2, size=size)
            self.arbitrage_opportunities.append((self.data.datetime.datetime(0), 'Buy QCLN, Sell QCLN2', size, -self.spread[0]))

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Create a data feed for QCLN ETF from 2010 to 2020
    start_date = '2010-01-01'
    end_date = '2020-12-31'
    qcln_data = bt.feeds.PandasData(dataname=yf.download('QCLN', start=start_date, end=end_date))
    qcln2_data = bt.feeds.PandasData(dataname=yf.download('SPY', start=start_date, end=end_date))

    # Add the data feed to the cerebro
    cerebro.adddata(qcln_data)
    cerebro.adddata(qcln2_data)

    # Add the trading strategy to the cerebro
    cerebro.addstrategy(QCLNStrategy)

    # Set the initial capital to $100,000
    cerebro.broker.setcash(100000.0)

    # Set the commission rate to 0.01%
    cerebro.broker.setcommission(commission=0.0001)

    # Run the backtest
    cerebro.run()

    # Sort the arbitrage opportunities by yield
    sorted_opportunities = sorted(cerebro.runstrats[0][0].arbitrage_opportunities, key=lambda x: x[3], reverse=True)

    # Print the top 10 arbitrage opportunities
    print('Top 10 arbitrage opportunities:')
    for opportunity in sorted_opportunities[:10]:
        print(opportunity[0].strftime('%Y-%m-%d %H:%M:%S'), opportunity[1], 'Size:', opportunity[2], 'Yield:', opportunity[3])

    # Plot the results
    cerebro.plot()
