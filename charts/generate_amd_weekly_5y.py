#!/usr/bin/env python3
"""Generate AMD weekly 5-year price chart for deep dive report"""

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

# Fetch AMD data - 5 years, weekly intervals
ticker = yf.Ticker("AMD")
df = ticker.history(period="5y", interval="1wk")

if df.empty:
    print("Failed to fetch data")
    exit(1)

print(f"Fetched {len(df)} weeks of data")
print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
print(f"Latest close: ${df['Close'].iloc[-1]:.2f}")

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), height_ratios=[3, 1], sharex=True)

# Plot price with moving averages
ax1.plot(df.index, df['Close'], color='#ff6b6b', linewidth=2.5, label='AMD Price')
ax1.plot(df.index, df['Close'].rolling(10).mean(), color='#f4a261', linewidth=2, label='10W MA (~50D)', alpha=0.9)
ax1.plot(df.index, df['Close'].rolling(20).mean(), color='#2a9d8f', linewidth=2, label='20W MA (~100D)', alpha=0.9)
ax1.plot(df.index, df['Close'].rolling(40).mean(), color='#264653', linewidth=2, label='40W MA (~200D)', alpha=0.9)

# Fill between for long-term context
ax1.fill_between(df.index, df['Low'], df['High'], alpha=0.1, color='#ff6b6b')

# Add key levels - all-time data
current_price = df['Close'].iloc[-1]
low_5y = df['Low'].min()
high_5y = df['High'].max()
ma_10w = df['Close'].rolling(10).mean().iloc[-1]
ma_20w = df['Close'].rolling(20).mean().iloc[-1]
ma_40w = df['Close'].rolling(40).mean().iloc[-1]

# Add horizontal lines for major levels
ax1.axhline(y=low_5y, color='#ff6b6b', linestyle='--', alpha=0.6, label=f'5Y Low: ${low_5y:.2f}')
ax1.axhline(y=high_5y, color='#00ff00', linestyle='--', alpha=0.6, label=f'5Y High: ${high_5y:.2f}')

# Mark major events/resistance levels
resistance_levels = [200, 150, 100]
for level in resistance_levels:
    if low_5y <= level <= high_5y:
        ax1.axhline(y=level, color='#ffd60a', linestyle=':', alpha=0.4, linewidth=1)

ax1.set_title('AMD - Weekly Chart (5 Years)', fontsize=18, fontweight='bold', pad=20)
ax1.set_ylabel('Price (USD)', fontsize=14)
ax1.legend(loc='upper left', fontsize=10, facecolor='#16213e', edgecolor='#4a7c59')

# Volume chart (weekly)
colors = ['#00ff00' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ff6b6b' for i in range(len(df))]
ax2.bar(df.index, df['Volume'], color=colors, alpha=0.7, width=5)  # Wider bars for weekly
ax2.set_ylabel('Volume', fontsize=12)
ax2.set_xlabel('Date', fontsize=12)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))

# Format x-axis for 5-year view
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=0)

# Add annotation for current price
ax1.annotate(f'Current: ${current_price:.2f}', 
             xy=(df.index[-1], current_price),
             xytext=(10, 20), textcoords='offset points',
             fontsize=12, color='#00ff00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00ff00', lw=1.5))

# Print technical levels
print(f"Current Price: ${current_price:.2f}")
print(f"10W MA (~50D): ${ma_10w:.2f}")
print(f"20W MA (~100D): ${ma_20w:.2f}")
print(f"40W MA (~200D): ${ma_40w:.2f}")
print(f"5-year Low: ${low_5y:.2f}")
print(f"5-year High: ${high_5y:.2f}")

plt.tight_layout()
plt.savefig('/home/ubuntu/clawd/Agent-Reports/charts/AMD-weekly-5y.png', 
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e', edgecolor='none')
print(f"Weekly 5Y chart saved to /home/ubuntu/clawd/Agent-Reports/charts/AMD-weekly-5y.png")