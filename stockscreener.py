import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get user input for the stock ticker to analyze
chosen_stock = input("Chosen stocks for analysis: ", )
data_check = yf.download(chosen_stock, period="1y", interval="1d", auto_adjust=False)

# Check if the chosen stock ticker is valid
if data_check.empty:
    print(f"The stock ticker '{chosen_stock}' is invalid or has no data available.")
else:
    

    # Going to start with tech stock, so my tickers will be the 15 majors stocks listed in NASDAQ
    tickers_15_NQ = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'META', 'AVGO', 'GOOGL', 'GOOG', 'TSLA', 'NFLX', 'PLTR', 'COST', 'AMD', 'ASML', 'CSCO']

    history_data = yf.download(tickers_15_NQ, period='1y', interval='1d', group_by='ticker', auto_adjust=False)

    if isinstance(history_data.columns, pd.MultiIndex):
        close_prices = history_data.xs('Close', level=1, axis=1)
    else:
        close_prices = history_data['Close']

    returns_nq100 = close_prices.dropna(how = 'all')

    # Analyze financial ratios for each stock in the top 15 NASDAQ tech stocks, and compare it with the chosen stock
    ratio = {}
    for i in tickers_15_NQ:
        stock = yf.Ticker(i)
        info = stock.info

        #Find Book to Market Ratio
        book_value_per_share_NQ = info.get('bookValue')
        price_NQ = stock.history(period="1d")['Close'].iloc[-1]
        if price_NQ and book_value_per_share_NQ != None:
            book_to_market_ratio_NQ = book_value_per_share_NQ / price_NQ
        else:
            book_to_market_ratio_NQ = None

        #Dictionary of ratios for each stock
        ratio[i] = {
            'Gross Margins': info.get('grossMargins'),
            'Operating Margins': info.get('operatingMargins'),
            'Return On Assets': info.get('returnOnAssets'),
            'Return On Equity': info.get('returnOnEquity'),
            'Trailing PE': info.get('trailingPE'),
            'Debt-to-Equity' :info.get('debtToEquity'),
            'Book to Market Ratio': book_to_market_ratio_NQ
        }

    # Display and mean financial ratios for the top 15 NASDAQ tech stocks
    ratio_graph = pd.DataFrame(ratio).T
    mean_ratios = ratio_graph.mean()
    print("\nMean Financial Ratios for Top 15 NASDAQ Tech Stocks:")
    print(mean_ratios)
    


    # Now analyze the chosen stock
    ratio_chosen_stock = {}
    stock_chosen_ratio = yf.Ticker(chosen_stock)
    info_chosen = stock_chosen_ratio.info

    #Find Book to Market Ratio
    book_value_per_share = info_chosen.get('bookValue')
    price = stock_chosen_ratio.history(period="1d")['Close'].iloc[-1]
    if price and book_value_per_share != None:
        book_to_market_ratio = book_value_per_share / price 
    else:
        book_to_market_ratio = None

    #Dictionary of chosen stock ratios
    ratio_chosen_stock[chosen_stock] = {
        'Gross Margins': info_chosen.get('grossMargins'),
        'Operating Margins': info_chosen.get('operatingMargins'),
        'Return On Assets': info_chosen.get('returnOnAssets'),
        'Return On Equity': info_chosen.get('returnOnEquity'),
        'Trailing PE': info_chosen.get('trailingPE'),
        'Debt-to-Equity' :info_chosen.get('debtToEquity'),
        'Book to Market Ratio': book_to_market_ratio
    }

    # Display financial ratios for the chosen stock
    ratio_graph_chosen_stock = pd.DataFrame(ratio_chosen_stock).T
    print(f"\nFinancial Ratios for Chosen Stock '{chosen_stock}':")
    print(ratio_graph_chosen_stock)
    print('')

    # Compare chosen stock ratios with mean ratios of top 15 NASDAQ tech stocks
    for ratio_name in mean_ratios.index:
        if ratio_graph_chosen_stock[ratio_name].values[0] is not None:
            if ratio_graph_chosen_stock[ratio_name].values[0] > mean_ratios[ratio_name]:
                print(f"{chosen_stock} has a higher {ratio_name} than the average of the top 15 NASDAQ tech stocks.")
            else:
                print(f"{chosen_stock} has a lower {ratio_name} than the average of the top 15 NASDAQ tech stocks.")
    


    # Simple value investing strategy to help for personal investment decision. Using Fama-French 3-Factor Model as reference.
    # Will create a score value based on the following criteria: 
    # High expected return (gives 2 points) : B/M ratio > 0.2 and trailing P/E ratio < 20
    # Medium expected return (gives 1 point): 0.1 > B/M ratio > 0.2 and 20 > trailing P/E ratio > 35
    # Low expected return (gives 0 point): B/M ratio < 0.1 and trailing P/E ratio > 35
    # Finally, sum the points to get a total score out of 4 (which would mean a 3/4 or higher would be a high expected return stock, 
    #       a 2/4 would be a medium expected return stock, and a 1/4 or less would be a low expected return stock, based off these ratios).
    # These thresholds are not based an any rigorous statistical analysis, but rather on general investing principles, do not take theses cutoffs seriously. 
    # A low value score does not necessarily mean a bad investment, just that it may not fit the value investing criteria well, and the price would already be priced for futur expectation.
    score = 0
    b_m_ratio = ratio_graph_chosen_stock['Book to Market Ratio'].values[0]
    trailing_pe = ratio_graph_chosen_stock['Trailing PE'].values[0]
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

        print(f"\nValue Investing Score for {chosen_stock}: {score}/4")
        if score >= 3:
            print("This stock is likely to have a high expected return based on the value investing criteria.")
        elif score == 2:
            print("This stock is likely to have a medium expected return based on the value investing criteria.")
        else:
            print("This stock is likely to have a low expected return based on the value investing criteria.")
    else:
        print("\nInsufficient data to calculate Value Investing Score.")
    

    graph_client = input("\nDo you want to see the stock price graph for the chosen stock? (yes/no): ", ).strip().lower()
    if graph_client == 'yes':
        data_check['Close'].plot(title=f'Daily Closing Prices for {chosen_stock} Over the Past Year', figsize=(10, 6))


        stock_graph = returns_nq100.plot(figsize=(14, 8), lw=1)
        stock_graph.set_title('Daily Charts of Major NASDAQ Tech Stocks Over the Past Year', fontsize=16)
        stock_graph.set_xlabel('Date', fontsize=14)
        stock_graph.set_ylabel('Price (USD)', fontsize=14)

        plt.show()