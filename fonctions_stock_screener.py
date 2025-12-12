# The fonctions used in my stock screener code
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Check the data of the chosen stock
def data_check(stock):
    """
    Check the data of the chosen stock

    Parameters 
    ----------
    stock : str
        The ticker symbol of the chosen stock 
    """
    return yf.download(stock, period="1y", interval="1d", auto_adjust=False)

# Check the data of the benchmark
def data_check_NQ(stock):
    """
    Check the data of the benchmark, group by tickers

    Parameters 
    ----------
    stock : str
        The ticker symbol of the benchmark
    """
    return yf.download(stock, period="1y", interval="1d", auto_adjust=False, group_by='ticker')

# Extract correctly the data of a couple of tickers (my benchmark)
def extract_close_prices(history_data):
    if isinstance(history_data.columns, pd.MultiIndex):
        close = history_data.xs('Close', level=1, axis=1)
    else:
        close = history_data['Close']

    return close.dropna(how='all')
    

def ratio_dictionnary(empty_dic,stock):
    """
    Create a dictionnary of the financial ratios of the chosen stock

    Parameters 
    ----------
    empty_dic : dictionnary
        An empty dictionnary to be replace with a dictionnary of all the financial ratios I want to analyse
    stock : str
        The ticker symbol of the chosen stock I want the financial ratios from
    """
    stock_ratio = yf.Ticker(stock)
    info = stock_ratio.info

    # Secure price extraction
    history = stock_ratio.history(period="1d")

    if history.empty or "Close" not in history.columns:
        print(f"⚠ Warning: No price data found for {stock}. Setting price to None.")
        price = None
    else:
        price = history["Close"].iloc[-1]

    # Compute Book-to-Market ratio safely
    book_value_per_share = info.get('bookValue')

    if price is not None and book_value_per_share is not None:
        book_to_market_ratio = book_value_per_share / price
    else:
        book_to_market_ratio = None

    # Build the dictionary
    empty_dic[stock] = {
        'Gross Margins': info.get('grossMargins'),
        'Operating Margins': info.get('operatingMargins'),
        'Return On Assets': info.get('returnOnAssets'),
        'Return On Equity': info.get('returnOnEquity'),
        'Trailing PE': info.get('trailingPE'),
        'Debt-to-Equity': info.get('debtToEquity'),
        'Book to Market Ratio': book_to_market_ratio
    }

    return empty_dic

def compare_ratios(chosen_stock, stock_ratios, benchmark_means):
    """
    Compares the ratios of a chosen stock to the mean ratios of a benchmark.

    Parameters
    ----------
    chosen_stock : str
        The ticker symbol of the chosen stock.
    stock_ratios : pandas.DataFrame
        DataFrame containing the ratios of the chosen stock (1 row).
    benchmark_means : pandas.Series
        Mean ratios of the benchmark (15 NASDAQ stocks in this case).

    Prints
    ------
    A message indicating whether each ratio is higher or lower than the benchmark mean.
    """

    for ratio_name in benchmark_means.index:
        value = stock_ratios[ratio_name].values[0]

        if value is not None:
            if value > benchmark_means[ratio_name]:
                print(f"{chosen_stock} has a HIGHER {ratio_name} than the benchmark average.")
            else:
                print(f"{chosen_stock} has a LOWER {ratio_name} than the benchmark average.")
    


def value_strategy(ratio_dic, stock):
    """
    Value Investing Score Strategy (inspired by Fama-French HML factor)

    Rules:
    - High expected return (2 points): B/M > 0.2 AND P/E < 20
    - Medium expected return (1 point): 0.1 < B/M <= 0.2 AND 20 <= P/E < 35
    - Low expected return (0 points): B/M <= 0.1 OR P/E >= 35

    Score: sum of points from both B/M and P/E → total out of 4.

    Note:
    These thresholds are simplified investing heuristics and not 
    statistically validated. A low score does not mean a stock is 
    “bad” but rather that it does not fit classic value-investing criteria.
    """
    score = 0
    b_m_ratio = ratio_dic['Book to Market Ratio'].values[0]
    trailing_pe = ratio_dic['Trailing PE'].values[0]
    if b_m_ratio != None and trailing_pe != None:
        if b_m_ratio > 0.2:
            score += 2
        elif 0.1 < b_m_ratio <= 0.2:
            score += 1
        elif b_m_ratio <= 0.1:
            score += 0

        if trailing_pe < 20:
            score += 2
        elif 20 <= trailing_pe < 35:
            score += 1
        elif trailing_pe >= 35:
            score += 0

        print(f"\nValue Investing Score for {stock}: {score}/4")
        if score >= 3:
            print("This stock is likely to have a high expected return based on the value investing criteria.")
        elif score == 2:
            print("This stock is likely to have a medium expected return based on the value investing criteria.")
        else:
            print("This stock is likely to have a low expected return based on the value investing criteria.")
    else:
        print("\nInsufficient data to calculate Value Investing Score.")
    return score


def plot_two_timeseries(df1, df2, title1, title2, figsize=(14, 10)):
    """
    Plot two time series one above the other using matplotlib.

    Parameters
    ----------
    df1 : pandas.Series or pandas.DataFrame
        The first time series to display (typically the chosen stock).
    df2 : pandas.DataFrame or pandas.Series
        The second time series to display (typically a benchmark or multiple tickers).
    title1 : str
        Title for the first subplot.
    title2 : str
        Title for the second subplot.
    figsize : tuple, optional
        Size of the overall matplotlib figure in inches. Default is (14, 10).

    Description
    -----------
    This function creates a figure with two subplots arranged vertically.
    - The first subplot displays df1 with a single line (if pandas Series) or multiple lines (if DataFrame).
    - The second subplot displays df2, also rendered with pandas' built-in `.plot()` method.
    
    This layout allows the user to compare a chosen stock's price evolution
    with a group of benchmark stocks (e.g., NASDAQ top 15) in a single matplotlib window.

    The function automatically adjusts spacing using `plt.tight_layout()`
    and displays the final figure with `plt.show()`.
    """

    fig, axes = plt.subplots(2, 1, figsize=figsize)

    # First graph (df1)
    axes[0].plot(df1.index, df1.values, lw=1.5)
    axes[0].set_title(title1, fontsize=14)
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Price")

    # Second graph (df2)
    df2.plot(ax=axes[1], lw=1)
    axes[1].set_title(title2, fontsize=14)
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Price")

    plt.tight_layout()
    plt.show()