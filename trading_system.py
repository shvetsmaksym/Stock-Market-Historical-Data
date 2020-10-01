import yfinance as yf

apple = yf.Ticker("AAPL")
print(apple)
#print(apple.info)
hist = apple.history(start="2020-09-01", end="2020-10-01")
print(hist)