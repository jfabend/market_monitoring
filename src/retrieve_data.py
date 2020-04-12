import pandas_datareader as pdr
import googlefinance as gf
import json
from urllib.request import Request
import yahoo_finance as yf
symbol = yf.Share("YHOO")
print(symbol.get_open())
#print(json.dumps(gf.getQuotes('AAPL'), indent=2))