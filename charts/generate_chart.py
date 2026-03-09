#!/usr/bin/env python3
"""Generate price chart for deep dive reports - Generic version

Usage: python generate_chart.py TICKER [output_path]
Example: python generate_chart.py AAPL charts/AAPL-price-2026-03-09.png
"""

import sys
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def generate_chart(ticker_symbol: str, output_path: str = None):
    """Generate a 1-year price chart with MAs and volume"""
    
    if output_path is None:
        today = datetime.now().strftime('%Y-%m-%d')
        output_path = f"{ticker_symbol}-price-{today}.png"
    
    # Set dark style
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

    # Fetch data
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="1y")

    if df.empty:
        print(f"Failed to fetch data for {ticker_symbol}")
        return None

    print(f"Fetched {len(df)} days of data for {ticker_symbol}")
    print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"Latest close: ${df['Close'].iloc[-1]:.2f}")

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1], sharex=True)

    # Plot price with moving averages
    ax1.plot(df.index, df['Close'], color='#4a7c59', linewidth=2, label='Price')
    
    if len(df) >= 50:
        ax1.plot(df.index, df['Close'].rolling(50).mean(), color='#f4a261', 
                 linewidth=1.5, label='50-day MA', alpha=0.8)
    if len(df) >= 200:
        ax1.plot(df.index, df['Close'].rolling(200).mean(), color='#e76f51', 
                 linewidth=1.5, label='200-day MA', alpha=0.8)

    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.set_title(f'{ticker_symbol} - 1 Year Price Chart', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', framealpha=0.9)

    # Add current price annotation
    current_price = df['Close'].iloc[-1]
    ax1.axhline(y=current_price, color='#4a7c59', linestyle='--', alpha=0.5)
    ax1.annotate(f'${current_price:.2f}', xy=(df.index[-1], current_price),
                 xytext=(10, 0), textcoords='offset points',
                 fontsize=10, color='#4a7c59', fontweight='bold')

    # 52-week high/low
    high_52w = df['High'].max()
    low_52w = df['Low'].min()
    ax1.axhline(y=high_52w, color='#2ecc71', linestyle=':', alpha=0.4)
    ax1.axhline(y=low_52w, color='#e74c3c', linestyle=':', alpha=0.4)

    # Plot volume
    colors = ['#2ecc71' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#e74c3c' 
              for i in range(len(df))]
    ax2.bar(df.index, df['Volume'], color=colors, alpha=0.7, width=0.8)
    ax2.set_ylabel('Volume', fontsize=12)

    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)

    # Add stats box
    stats_text = f"52W High: ${high_52w:.2f}\n52W Low: ${low_52w:.2f}\nCurrent: ${current_price:.2f}"
    props = dict(boxstyle='round', facecolor='#16213e', alpha=0.9, edgecolor='#4a7c59')
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()
    
    print(f"Chart saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_chart.py TICKER [output_path]")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = generate_chart(ticker, output)
    if result is None:
        sys.exit(1)
