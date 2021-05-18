# Retrieve the inflation data from here:
# https://inflationdata.com/Inflation/Inflation_Rate/HistoricalInflation.aspx
# (I saved it to a local csv)

# Here is explained how you can reshape it:
# https://stackoverflow.com/questions/40136651/stack-output-with-all-individual-indexs-filled-in-pandas-dataframe

#%%
import pandas as pd
inflation_raw = pd.read_csv("C:\\Data\\Trading\\Inflationsraten.csv", sep = ",")
inflation_raw = inflation_raw.set_index('Jahr')
#%%
# Stack the df
pd.set_option('display.multi_sparse', False)
infl_df = pd.DataFrame(inflation_raw.stack())

# %%
df = infl_df.reset_index()
df.columns = ['year', 'month', 'value']
df = df[df['month'] != 'Durchschnitt']
# %%
# new date column
df['date'] = df.apply(lambda x: f"01.{x['month']}.{x['year']}", axis=1)
# %%
# Put date column at first place and drop year and month
df = df.drop(['year', 'month'], axis=1)
df = df[['date', 'value']]
# %%
df.to_csv("C:\\Data\\Trading\\market_monitoring\\data\\us_inflation_rate_monthly\\20210518.csv",
sep = ",", index=False)
# %%
