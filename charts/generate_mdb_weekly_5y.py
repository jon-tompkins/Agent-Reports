#!/usr/bin/env python3
"""Generate MDB weekly 5-year price chart for deep dive report"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#16213e'
plt.rcParams['axes.edgecolor'] = '#4a7c59'
plt.rcParams['axes.labelcolor'] = '#edf2f4'
plt.rcParams['text.color'] = '#edf2f4'
plt.rcParams['xtick.color'] = '#edf2f4'
plt.rcParams['ytick.color'] = '#edf2f4'
plt.rcParams['grid.color'] = '#0f3460'
plt.rcParams['grid.alpha'] = 0.5

# Fetch MDB data - 5 years
ticker = yf.Ticker("MDB")
df = ticker.history(period="5y")

if df.empty:
    print("Failed to fetch data")
    exit(1)

# Resample to weekly data (Friday close)
weekly_df = df.resample('W-FRI').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
}).dropna()

print(f"Fetched {len(weekly_df)} weeks of data")
print(f"Date range: {weekly_df.index[0].strftime('%Y-%m-%d')} to {weekly_df.index[-1].strftime('%Y-%m-%d')}")
print(f"Latest close: ${weekly_df['Close'].iloc[-1]:.2f}")

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1], sharex=True)

# Plot price with moving averages
ax1.plot(weekly_df.index, weekly_df['Close'], color='#ff6b6b', linewidth=2, label='MDB Price')
ax1.plot(weekly_df.index, weekly_df['Close'].rolling(10).mean(), color='#f4a261', linewidth=2, label='10-week MA', alpha=0.9)
ax1.plot(weekly_df.index, weekly_df['Close'].rolling(20).mean(), color='#2a9d8f', linewidth=2, label='20-week MA', alpha=0.9)
ax1.plot(weekly_df.index, weekly_df['Close'].rolling(50).mean(), color='#264653', linewidth=2, label='50-week MA', alpha=0.9)

# Fill between for context
ax1.fill_between(weekly_df.index, weekly_df['Low'], weekly_df['High'], alpha=0.1, color='#ff6b6b')

# Add key technical levels
current_price = weekly_df['Close'].iloc[-1]
low_52wk = weekly_df['Low'].tail(52).min()  # Last 52 weeks
high_52wk = weekly_df['High'].tail(52).max()  # Last 52 weeks
ma_10w = weekly_df['Close'].rolling(10).mean().iloc[-1]
ma_20w = weekly_df['Close'].rolling(20).mean().iloc[-1]
ma_50w = weekly_df['Close'].rolling(50).mean().iloc[-1]

# Add horizontal lines for key levels
ax1.axhline(y=low_52wk, color='#ff6b6b', linestyle='--', alpha=0.6, label=f'52W Low: ${low_52wk:.2f}')
ax1.axhline(y=high_52wk, color='#00ff00', linestyle='--', alpha=0.6, label=f'52W High: ${high_52wk:.2f}')

ax1.set_title('MDB (MongoDB) - Weekly Chart (5 Years)', fontsize=18, fontweight='bold', pad=20)
ax1.set_ylabel('Price (USD)', fontsize=14)
ax1.legend(loc='upper left', fontsize=10, facecolor='#16213e', edgecolor='#4a7c59')

# Volume chart
colors = ['#00ff00' if weekly_df['Close'].iloc[i] >= weekly_df['Open'].iloc[i] else '#ff6b6b' for i in range(len(weekly_df))]
ax2.bar(weekly_df.index, weekly_df['Volume'], color=colors, alpha=0.7, width=5)
ax2.set_ylabel('Volume', fontsize=12)
ax2.set_xlabel('Date', fontsize=12)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))

# Format x-axis
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=45)

# Add annotation for current price
ax1.annotate(f'Current: ${current_price:.2f}', 
             xy=(weekly_df.index[-1], current_price),
             xytext=(10, 20), textcoords='offset points',
             fontsize=12, color='#00ff00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00ff00', lw=1.5))

# Print technical levels
print(f"Current Price: ${current_price:.2f}")
print(f"10-week MA: ${ma_10w:.2f}")
print(f"20-week MA: ${ma_20w:.2f}")
print(f"50-week MA: ${ma_50w:.2f}")
print(f"52-week Low: ${low_52wk:.2f}")
print(f"52-week High: ${high_52wk:.2f}")

plt.tight_layout()
plt.savefig('/home/ubuntu/clawd/Agent-Reports/charts/MDB-weekly-5y.png', 
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e', edgecolor='none')
print(f"Weekly 5Y chart saved to /home/ubuntu/clawd/Agent-Reports/charts/MDB-weekly-5y.png")