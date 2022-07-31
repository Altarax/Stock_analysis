from asyncio.windows_events import NULL
import yfinance as yf
import matplotlib.pyplot as plt

amundi = yf.Ticker("UBI.PA")
if (amundi.dividends.empty):
    plt.figure()
    plt.plot(NULL)
    plt.savefig(f'stocks/static/images/dividend_price_{"ubisoft"}.png')