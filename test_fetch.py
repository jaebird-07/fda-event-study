import yfinance as yf
import pandas as pd

data = yf.download("AZN", start="2026-07-01", end="2026-07-20", auto_adjust=True)
print(data)

close_prices = data["Close"]
print(close_prices)
print(type(close_prices))

azn_close = close_prices["AZN"]
print(azn_close)
print(type(azn_close))

data = yf.download("^GSPC", start="2026-07-01", end="2026-07-20", auto_adjust=True)
print(data)

close_prices = data["Close"]
print(close_prices)
print(type(close_prices))

gspc_close = close_prices["^GSPC"]
print(gspc_close)
print(type(gspc_close))

combined = pd.concat([azn_close, gspc_close], axis=1)
print(combined)

returns = combined.pct_change()
print(returns)