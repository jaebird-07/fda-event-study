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

event_idx = returns.index.get_loc("2026-07-14")
print(event_idx)

estimation_window = returns.iloc[6:206]
print("Estimation window:")
print(estimation_window.index[0])
print(estimation_window.index[-1])

pre_event = returns.iloc[206:216]
print("Pre-event window:")
print(pre_event.index[0])
print(pre_event.index[-1])

event_window = returns.iloc[215:218]
print("Event window:")
print(event_window.index[0])
print(event_window.index[-1])

post_event = returns.iloc[218:227]
print("Post-event window:")
print(post_event.index[0])
print(post_event.index[-1])

from scipy.stats import linregress

result = linregress(estimation_window["^GSPC"], estimation_window["AZN"])
print("beta:", result.slope)
print("alpha:", result.intercept)

predicted_AZN = result.intercept + result.slope * event_window["^GSPC"]
abnormal_return = event_window["AZN"] - predicted_AZN
print("Abnormal return in event window:")
print(abnormal_return)