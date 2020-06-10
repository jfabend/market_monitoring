#%%
import yfinance as yf
xyl = yf.Ticker("XYL")
xyl.info

# %%
xyl.dividends

# %%
xyl_info_dict = xyl.info
xyl_info_dict.keys()
xyl_info_dict['dividendYield']
# %%
xyl_info_dict['pegRatio']

# %%
msft = yf.Ticker("MSFT")
msft.quarterly_earnings

# %%
