# Library imports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dtime

# Read data files
df_btc_price = pd.read_csv('Data/Bitcoin Historical Data 2024.csv')
df_btc_trends = pd.read_csv('Data/multiTimeline 2024.csv',
                            skiprows=2)

# Clean and format data
df_btc_price.drop(columns=['Open', 'High', 'Low', 'Vol.', 'Change %'],
                  inplace=True)
df_btc_trends.rename(columns={"Month": "Date", "Bitcoin: (Worldwide)": "Search NO."}, inplace=True)

# Date format
df_btc_price.Date = pd.to_datetime(df_btc_price.Date)
df_btc_trends.Date = pd.to_datetime(df_btc_trends.Date)

df_btc_price["Price"] = df_btc_price["Price"].str.replace(',', '').astype(float)
df_btc_trends["Search NO."] = pd.to_numeric(df_btc_trends["Search NO."].replace("<1", 0))

df_btc_price = df_btc_price.resample(rule="ME", on="Date").last()
df_btc_trends = df_btc_trends.resample(rule="ME", on="Date").last()

# Merge data
df_btc_data = pd.merge(df_btc_price, df_btc_trends, left_index=True, right_index=True, how="inner").reset_index()
df_btc_data.rename(columns={"index": "Date"}, inplace=True)

# Graph details
plt.figure(dpi=120, figsize=(15, 8))
plt.title("Bitcoin Price and Search Trend (2010-2023)", fontsize=18)

year_major = dtime.YearLocator()
month_minor = dtime.MonthLocator()
year_formatter = dtime.DateFormatter("%Y")

ax1 = plt.gca()
ax2 = ax1.twinx()

# Draw graph
ax1.plot(df_btc_data["Date"], df_btc_data["Price"], lw=0.5, label="Price", color="green", ls="dashed")
ax2.plot(df_btc_data["Date"], df_btc_data["Search NO."], lw=0.5, label="Search", color="red", marker="o", markersize=3)
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

ax1.set_xlabel("Date")
ax1.set_ylabel("Price", color="green", fontsize=14)
ax2.set_ylabel("Search", color="red", fontsize=14)
ax1.set_ylim(0, df_btc_data["Price"].max() * 1.1)
ax2.set_ylim(0, df_btc_data["Search NO."].max() * 1.1)

ax1.xaxis.set_major_locator(year_major)
ax1.xaxis.set_minor_locator(month_minor)
ax1.xaxis.set_major_formatter(year_formatter)

plt.show()
