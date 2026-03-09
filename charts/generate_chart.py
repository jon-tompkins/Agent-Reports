#!/usr/bin/env python3
"""Generate price charts for deep dive reports

Usage: 
  python generate_chart.py TICKER              # Generates both daily-2y and weekly-5y
  python generate_chart.py TICKER daily        # Daily 2Y only
  python generate_chart.py TICKER weekly       # Weekly 5Y only
  
Output:
  TICKER-daily-2y.png   - 2 year daily chart with 50/200 MAs
  TICKER-weekly-5y.png  - 5 year weekly chart with 50/200 MAs
"""

import sys
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def setup_style():
    """Dark theme matching report style"""
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

def generate_chart(ticker_symbol: str, period: str = "2y", interval: str = "1d", 
                   output_path: str = None, title_suffix: str = "Daily 2Y"):
    """Generate a price chart with MAs and volume"""
    
    setup_style()
    
    # Fetch data
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period, interval=interval)

    if df.empty:
        print(f"Failed to fetch data for {ticker_symbol}")
        return None

    print(f"Fetched {len(df)} bars for {ticker_symbol} ({period}, {interval})")
    print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"Latest close: ${df['Close'].iloc[-1]:.2f}")

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1], sharex=True)

    # Plot price with moving averages
    ax1.plot(df.index, df['Close'], color='#4a7c59', linewidth=2, label='Price')
    
    # Adjust MA periods for weekly charts
    ma_short = 10 if interval == "1wk" else 50
    ma_long = 40 if interval == "1wk" else 200
    
    if len(df) >= ma_short:
        ax1.plot(df.index, df['Close'].rolling(ma_short).mean(), color='#f4a261', 
                 linewidth=1.5, label=f'{ma_short}-period MA', alpha=0.8)
    if len(df) >= ma_long:
        ax1.plot(df.index, df['Close'].rolling(ma_long).mean(), color='#e76f51', 
                 linewidth=1.5, label=f'{ma_long}-period MA', alpha=0.8)

    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.set_title(f'{ticker_symbol} - {title_suffix}', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', framealpha=0.9)

    # Add current price annotation
    current_price = df['Close'].iloc[-1]
    ax1.axhline(y=current_price, color='#4a7c59', linestyle='--', alpha=0.5)
    ax1.annotate(f'${current_price:.2f}', xy=(df.index[-1], current_price),
                 xytext=(10, 0), textcoords='offset points',
                 fontsize=10, color='#4a7c59', fontweight='bold')

    # 52-week high/low (or period high/low for weekly)
    high_period = df['High'].max()
    low_period = df['Low'].min()
    ax1.axhline(y=high_period, color='#2ecc71', linestyle=':', alpha=0.4)
    ax1.axhline(y=low_period, color='#e74c3c', linestyle=':', alpha=0.4)

    # Plot volume
    colors = ['#2ecc71' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#e74c3c' 
              for i in range(len(df))]
    ax2.bar(df.index, df['Volume'], color=colors, alpha=0.7, width=0.8)
    ax2.set_ylabel('Volume', fontsize=12)

    # Format x-axis based on timeframe
    if interval == "1wk":
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax2.xaxis.set_major_locator(mdates.YearLocator())
    else:
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    # Add stats box
    stats_text = f"High: ${high_period:.2f}\nLow: ${low_period:.2f}\nCurrent: ${current_price:.2f}"
    props = dict(boxstyle='round', facecolor='#16213e', alpha=0.9, edgecolor='#4a7c59')
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()
    
    print(f"Chart saved to: {output_path}")
    return output_path


def generate_daily_2y(ticker: str):
    """Generate 2-year daily chart"""
    output = f"{ticker}-daily-2y.png"
    return generate_chart(ticker, period="2y", interval="1d", 
                         output_path=output, title_suffix="Daily 2Y")


def generate_weekly_5y(ticker: str):
    """Generate 5-year weekly chart"""
    output = f"{ticker}-weekly-5y.png"
    return generate_chart(ticker, period="5y", interval="1wk", 
                         output_path=output, title_suffix="Weekly 5Y")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_chart.py TICKER [daily|weekly|both]")
        print("  daily  - 2 year daily chart")
        print("  weekly - 5 year weekly chart") 
        print("  both   - both charts (default)")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    chart_type = sys.argv[2].lower() if len(sys.argv) > 2 else "both"
    
    if chart_type in ["daily", "both"]:
        generate_daily_2y(ticker)
    
    if chart_type in ["weekly", "both"]:
        generate_weekly_5y(ticker)
    
    if chart_type == "both":
        print(f"\nEmbed in report:")
        print(f"![{ticker} Daily 2Y](../charts/{ticker}-daily-2y.png)")
        print(f"![{ticker} Weekly 5Y](../charts/{ticker}-weekly-5y.png)")
