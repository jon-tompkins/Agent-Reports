#!/usr/bin/env python3
"""Generate AES price chart for deep dive report"""

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

# Fetch AES data - 1 year
ticker = yf.Ticker("AES")
df = ticker.history(period="1y")

if df.empty:
    print("Failed to fetch data")
    exit(1)

print(f"Fetched {len(df)} days of data")
print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
print(f"Latest close: ${df['Close'].iloc[-1]:.2f}")

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1], sharex=True)

# Plot price with 50-day and 200-day moving averages
ax1.plot(df.index, df['Close'], color='#4a7c59', linewidth=2, label='Price')
ax1.plot(df.index, df['Close'].rolling(50).mean(), color='#f4a261', linewidth=1.5, label='50-day MA', alpha=0.8)
ax1.plot(df.index, df['Close'].rolling(200).mean(), color='#e76f51', linewidth=1.5, label='200-day MA', alpha=0.8)

# Fill between for context
ax1.fill_between(df.index, df['Low'], df['High'], alpha=0.2, color='#4a7c59')

# Add key levels - 52 week range
low_52wk = df['Low'].min()
high_52wk = df['High'].max()
ax1.axhline(y=low_52wk, color='#ff6b6b', linestyle='--', alpha=0.5, label=f'52-week Low (${low_52wk:.2f})')
ax1.axhline(y=high_52wk, color='#00ff00', linestyle='--', alpha=0.5, label=f'52-week High (${high_52wk:.2f})')

ax1.set_title('AES (AES Corporation) - 1 Year Price Chart', fontsize=16, fontweight='bold', pad=20)
ax1.set_ylabel('Price (USD)', fontsize=12)
ax1.legend(loc='upper left', fontsize=9, facecolor='#16213e', edgecolor='#4a7c59')
ax1.set_ylim([min(df['Low']) * 0.95, max(df['High']) * 1.05])

# Volume chart
colors = ['#00ff00' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ff6b6b' for i in range(len(df))]
ax2.bar(df.index, df['Volume'], color=colors, alpha=0.7, width=0.8)
ax2.set_ylabel('Volume', fontsize=12)
ax2.set_xlabel('Date', fontsize=12)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))

# Format x-axis
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45)

# Add annotation for current price
current_price = df['Close'].iloc[-1]
current_date = df.index[-1]
ax1.annotate(f'${current_price:.2f}', 
             xy=(current_date, current_price),
             xytext=(10, 10), textcoords='offset points',
             fontsize=11, color='#00ff00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00ff00', lw=1.5))

plt.tight_layout()
plt.savefig('/home/ubuntu/clawd/Agent-Reports/charts/aes-price-2026-02-07.png', 
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e', edgecolor='none')
print(f"Chart saved to /home/ubuntu/clawd/Agent-Reports/charts/aes-price-2026-02-07.png")