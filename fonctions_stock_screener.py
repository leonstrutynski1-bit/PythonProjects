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
    Check the data of the sample, group by tickers

    Parameters 
    ----------
    stock : str
        The ticker symbol of the sample
    """
    return yf.download(stock, period="1y", interval="1d", auto_adjust=False, group_by='ticker')

# Extract correctly the data of a couple of tickers (sample)
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
        print(f"Warning: No price data found for {stock}. Setting price to None.")
        price = None
    else:
        price = history["Close"].iloc[-1]

    # Compute Book-to-Price ratio
    book_value_per_share = info.get('bookValue')

    if price is not None and book_value_per_share is not None:
        book_to_price_ratio = book_value_per_share / price
    else:
        book_to_price_ratio = None

    # Build the dictionary
    empty_dic[stock] = {
        'Gross Margins': info.get('grossMargins'),
        'Operating Margins': info.get('operatingMargins'),
        'Return On Assets': info.get('returnOnAssets'),
        'Return On Equity': info.get('returnOnEquity'),
        'Trailing PE': info.get('trailingPE'),
        'Debt-to-Equity': info.get('debtToEquity'),
        'Book to Price Ratio': book_to_price_ratio
    }

    return empty_dic

def compare_ratios(chosen_stock, stock_ratios, sample_means):
    """
    Compares the ratios of a chosen stock to the mean ratios of the sample.

    Parameters
    ----------
    chosen_stock : str
        The ticker symbol of the chosen stock.
    stock_ratios : pandas.DataFrame
        DataFrame containing the ratios of the chosen stock (1 row).
    sample_means : pandas.Series
        Mean ratios of the sample (15 NASDAQ stocks in this case).

    Prints
    ------
    A message indicating whether each ratio is higher or lower than the sample mean.
    """

    for ratio_name in sample_means.index:
        value = stock_ratios[ratio_name].values[0]

        if value is not None:
            if value > sample_means[ratio_name]:
                print(f"{chosen_stock} has a HIGHER {ratio_name} than the sample average.")
            else:
                print(f"{chosen_stock} has a LOWER {ratio_name} than the sample average.")
    


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
    b_m_ratio = ratio_dic['Book to Price Ratio'].values[0]
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


def _to_series(x, name=None):
    """Convert Series/DataFrame(1 col)/array-like to a pandas Series."""
    if isinstance(x, pd.DataFrame):
        if x.shape[1] == 1:
            s = x.iloc[:, 0].copy()
            if name:
                s.name = name
            return s
        raise ValueError("Expected a Series or a single-column DataFrame for this input.")
    if isinstance(x, pd.Series):
        s = x.copy()
        if name:
            s.name = name
        return s
    return pd.Series(x, name=name)

def _normalize_to_100(series_or_df):
    """Normalize price series (or each column in df) to start at 100."""
    if isinstance(series_or_df, pd.Series):
        base = series_or_df.dropna().iloc[0]
        return (series_or_df / base) * 100.0
    elif isinstance(series_or_df, pd.DataFrame):
        out = series_or_df.copy()
        for c in out.columns:
            col = out[c].dropna()
            if len(col) == 0:
                out[c] = pd.NA
            else:
                out[c] = (out[c] / col.iloc[0]) * 100.0
        return out
    else:
        raise TypeError("Expected pandas Series or DataFrame.")

def plot_stock_universe_benchmark(
    chosen_prices,
    universe_prices,
    benchmark_prices,
    chosen_label="Chosen Stock",
    benchmark_label="QQQ",
    title_universe="Universe (15 stocks)",
    normalize=True,
    figsize=(14, 11),
    max_universe_lines=15
):
    """
    Plot 3 stacked charts:
      1) chosen stock
      2) universe of stocks (DataFrame columns = tickers)
      3) benchmark (QQQ)

    Parameters
    ----------
    chosen_prices : pd.Series or single-col DataFrame
        Price series of the chosen stock.
    universe_prices : pd.DataFrame
        Price series of the universe (columns=tickers).
    benchmark_prices : pd.Series or single-col DataFrame
        Price series of benchmark ETF (QQQ).
    normalize : bool
        If True, rebases each series to 100 at the first available date.
    max_universe_lines : int
        Safety to avoid plotting hundreds of tickers by accident.
    """

    # Convert & clean
    chosen = _to_series(chosen_prices, name=chosen_label).dropna()
    bench = _to_series(benchmark_prices, name=benchmark_label).dropna()

    if not isinstance(universe_prices, pd.DataFrame):
        raise TypeError("universe_prices must be a pandas DataFrame with columns=tickers.")

    universe = universe_prices.copy().dropna(how="all").ffill()

    # Safety: limit universe lines
    if universe.shape[1] > max_universe_lines:
        universe = universe.iloc[:, :max_universe_lines]

    # Align dates (intersection)
    common_idx = chosen.index.intersection(universe.index).intersection(bench.index)
    chosen = chosen.loc[common_idx]
    universe = universe.loc[common_idx]
    bench = bench.loc[common_idx]

    if normalize:
        chosen_plot = _normalize_to_100(chosen)
        universe_plot = _normalize_to_100(universe)
        bench_plot = _normalize_to_100(bench)
        ylab = "Indexed Price (Start=100)"
    else:
        chosen_plot = chosen
        universe_plot = universe
        bench_plot = bench
        ylab = "Price"

    fig, axes = plt.subplots(3, 1, figsize=figsize)

    # 1) chosen
    axes[0].plot(chosen_plot.index, chosen_plot.values, lw=1.6)
    axes[0].set_title(f"{chosen_label}", fontsize=14)
    axes[0].set_ylabel(ylab)

    # 2) universe
    universe_plot.plot(ax=axes[1], lw=1, legend=False)
    axes[1].set_title(title_universe, fontsize=14)
    axes[1].set_ylabel(ylab)

    # 3) benchmark
    axes[2].plot(bench_plot.index, bench_plot.values, lw=1.6)
    axes[2].set_title(f"Benchmark ({benchmark_label})", fontsize=14)
    axes[2].set_ylabel(ylab)
    axes[2].set_xlabel("Date")

    plt.tight_layout()
    plt.show()