import pandas as pd

# Create dim_time with hours as smallest unit
# (freq=H)
def create_date_table2_hour_level(start=pd.Timestamp(year=1920, month=1, day=1, hour=0), end=pd.Timestamp(year=2050, month=12, day=31, hour=23)):
     df = pd.DataFrame({"Date": pd.date_range(start, end, freq='H')})
     df["Weekday"] = df.Date.dt.weekday_name
     df["Week"] = df.Date.dt.weekofyear
     df["Quarter"] = df.Date.dt.quarter
     df["Year"] = df.Date.dt.year
     df["Month"] = df.Date.dt.month
     df["Monthday"] = df.Date.dt.day
     df["hour"] = df.Date.dt.hour
     df["Year_half"] = (df.Quarter + 1) // 2
     df["Date_notime"] = df.Date.dt.date
     return df

# Create dim_time with date as smallest unit
# (freq=D)
def create_date_table2_date_level(start=pd.Timestamp(year=1920, month=1, day=1), end=pd.Timestamp(year=2050, month=12, day=31)):
     df = pd.DataFrame({"Date": pd.date_range(start, end, freq='D')})
     df["Weekday"] = df.Date.dt.weekday_name
     df["Week"] = df.Date.dt.weekofyear
     df["Quarter"] = df.Date.dt.quarter
     df["Year"] = df.Date.dt.year
     df["Month"] = df.Date.dt.month
     df["Monthday"] = df.Date.dt.day
     df["Year_half"] = (df.Quarter + 1) // 2
     return df

dim_time_df = create_date_table2_date_level()
#print(dim_time_df.sample(5))

dim_time_df.to_csv('C:\Data\Trading\market_monitoring\dim_time\dim_time.csv', index=False)  

