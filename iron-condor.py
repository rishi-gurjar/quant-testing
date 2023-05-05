import backtrader as bt
import yfinance as yf
import datetime as dt

class IronCondorStrategy(bt.Strategy):
    params = (
        ("short_call_strike", None),
        ("long_call_strike", None),
        ("short_put_strike", None),
        ("long_put_strike", None),
        ("expiration_date", None),
        ("quantity", None)
    )

    def __init__(self):
        self.short_call = None
        self.long_call = None
        self.short_put = None
        self.long_put = None

    def next(self):
        pass

    def start(self):
        self.startcash = self.broker.getvalue()

        # Get the underlying asset price data
        ticker = self.getdatanames()[0]
        asset = yf.Ticker(ticker)
        self.underlying_price_data = asset.history(period="1d", start=self.datas[0].datetime.date(0), end=self.p.expiration_date)

        # Get the option chains for the expiration date
        self.options = asset.option_chain(date=self.p.expiration_date)

        # Filter for the specific strikes
        self.short_call = self.options.calls[self.options.calls["strike"] == self.p.short_call_strike]
        self.long_call = self.options.calls[self.options.calls["strike"] == self.p.long_call_strike]
        self.short_put = self.options.puts[self.options.puts["strike"] == self.p.short_put_strike]
        self.long_put = self.options.puts[self.options.puts["strike"] == self.p.long_put_strike]

        # Get the option prices
        self.short_call_price = self.short_call.iloc[0]["lastPrice"]
        self.long_call_price = self.long_call.iloc[0]["lastPrice"]
        self.short_put_price = self.short_put.iloc[0]["lastPrice"]
        self.long_put_price = self.long_put.iloc[0]["lastPrice"]

        # Calculate the profit/loss at expiration
        self.max_profit = self.short_call_price + self.long_put_price + self.short_put_price + self.long_call_price
        self.max_loss = self.long_call_strike - self.short_call_strike - self.max_profit
        self.break_even_high = self.short_call_strike + self.max_profit
        self.break_even_low = self.short_put_strike - self.max_profit

        # Log the option prices and P/L calculations
        self.log(f"Short call price: {self.short_call_price:.2f}")
        self.log(f"Long call price: {self.long_call_price:.2f}")
        self.log(f"Short put price: {self.short_put_price:.2f}")
        self.log(f"Long put price: {self.long_put_price:.2f}")
        self.log(f"Max profit: {self.max_profit:.2f}")
        self.log(f"Max loss: {self.max_loss:.2f}")
        self.log(f"Break-even high: {self.break_even_high:.2f}")
        self.log(f"Break-even low: {self.break_even_low:.2f}")

    def stop(self):
        self.roi = (self.broker.getvalue() / self.startcash) - 1.0
        self.log(f"ROI: {self.roi:.2%}")

        # Plot the underlying asset price data
        p1 = bt.plotting.Plot(title="Underlying Asset")
        p1.plot(self.datas[0])

        # Plot the option chains
        p2 = bt.plotting.Plot(title="Option Chains")
        p2.plot(self.short_call, color="red", width=2)