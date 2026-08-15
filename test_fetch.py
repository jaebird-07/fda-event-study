import yfinance as yf
import pandas as pd

data = yf.download("AZN", start="2025-09-01", end="2026-07-31", auto_adjust=True)
print(data)

close_prices = data["Close"]
print(close_prices)
print(type(close_prices))

azn_close = close_prices["AZN"]
print(azn_close)
print(type(azn_close))

data = yf.download("^GSPC", start="2025-09-01", end="2026-07-31", auto_adjust=True)
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

combined.to_csv("data/azn_gspc_prices.csv")
returns.to_csv("data/azn_gspc_returns.csv")
