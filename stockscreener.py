# First python code. Simple stock screener for comparaison of financial ratios to help with personnal stock picking
# Need to pay attention for correct typo while typing stock ticker
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fonctions_stock_screener

# Get user input for the stock ticker to analyze
chosen_stock = input("Chosen stocks for analysis: ", )
data_check = fonctions_stock_screener.data_check(chosen_stock)

# Check if the chosen stock ticker is valid
if data_check.empty:
    print(f"The stock ticker '{chosen_stock}' is invalid or has no data available.")
else:
    # Going to start with tech stock, so my tickers will be the 15 majors stocks listed in NASDAQ
    tickers_15_NQ = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'META', 'AVGO', 'GOOGL', 'GOOG', 'TSLA', 'NFLX', 'PLTR', 'COST', 'AMD', 'ASML', 'CSCO']
    history_data = fonctions_stock_screener.data_check_NQ(tickers_15_NQ)

    # Correctly extract the data of the 15 tickers
    returns_nq100 = fonctions_stock_screener.extract_close_prices(history_data)

    # Analyze financial ratios for each stock in the top 15 NASDAQ tech stocks, and compare it with the chosen stock
    ratio_NQ = {}
    for i in tickers_15_NQ:
       ratio_NQ = fonctions_stock_screener.ratio_dictionnary(ratio_NQ, i)

    # Display and mean financial ratios for the top 15 NASDAQ tech stocks
    ratio_graph = pd.DataFrame(ratio_NQ).T
    print(ratio_graph)
    mean_ratios = ratio_graph.mean()
    print("\nMean Financial Ratios for Top 15 NASDAQ Tech Stocks:")
    print(mean_ratios)
    
    # Now analyze the chosen stock
    ratio_chosen_stock = {}
    ratio_chosen_stock = fonctions_stock_screener.ratio_dictionnary(ratio_chosen_stock, chosen_stock)
    
    # Display financial ratios for the chosen stock
    ratio_graph_chosen_stock = pd.DataFrame(ratio_chosen_stock).T
    print(f"\nFinancial Ratios for Chosen Stock '{chosen_stock}':")
    print(ratio_graph_chosen_stock)
    print('')

    # Compare chosen stock ratios with mean ratios of top 15 NASDAQ tech stocks
    fonctions_stock_screener.compare_ratios(chosen_stock, ratio_graph_chosen_stock, mean_ratios)
    
    # My value investing strategy inspired by the Fama-French HML (High Minus Low) factor.
    # The score (out of 4) is based on two value metrics: Book-to-Price and Trailing P/E.
    # Higher scores indicate stocks that are cheaper relative to their fundamentals, not necessarily safer or better companies.
    # Lower scores indicate stocks that are more expensive or growth-oriented, not necessarily low risk.
    #
    # This strategy is NOT statistically backtested yet and should be used with caution.
    # It is meant as a simple screening tool rather than an automatic buy/sell signal.
    # I plan to backtest this approach in the future on a larger dataset with more advanced techniques.
    #
    # Note: Book-to-Price may be a weak metric for technology stocks because much of their value is intangible
    # (software, data, patents, brand, R&D), which is not fully captured in book value.
    # Therefore, results should be interpreted carefully, especially in the tech sector.
    score_value_investing = fonctions_stock_screener.value_strategy(ratio_graph_chosen_stock, chosen_stock)

    # Display the value investing score of all the benchmark stocks
    value_investing_momentum = input("\nDo you want to see the Value Investing score of all the benchmark stocks? (yes/no): ", ).strip().lower()
    if value_investing_momentum == 'yes':
        for holding in tickers_15_NQ:
            ratio_row = ratio_graph.loc[[holding]]
            score = fonctions_stock_screener.value_strategy(ratio_row, holding)
            
            
    
    # Showing the graph of the chosen stock, the sample and the benchmark (QQQ) only if we say yes to the terminal
    while True : 
        graph_client = input("\nDo you want to see the stock price graph for the chosen stock? (yes/no): ", ).strip().lower()
        if graph_client == 'yes':
            qqq = yf.download("QQQ", period="1y", interval="1d", auto_adjust=True)["Close"]
            fonctions_stock_screener.plot_stock_universe_benchmark(
                chosen_prices=data_check["Close"],          
                universe_prices=returns_nq100,              
                benchmark_prices=qqq,
                chosen_label=chosen_stock.upper(),
                benchmark_label="QQQ",
                title_universe="Top 15 NASDAQ (sample)",
                normalize=True
            )
        elif graph_client == 'no':
            break
        else:
            print('Invalid awnser')