# Building a python code for option pricing with the Black-Scholes formula. 
# Test to see if commit on github works
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import fonctions_option_pricing
import fonctions_stock_screener


chosen_stock = input("Chosen stocks for analysis: ",).strip().upper()
data_check = fonctions_stock_screener.data_check(chosen_stock)

if data_check.empty:
    print(f"The stock ticker '{chosen_stock}' is invalid or has no data available.")
else:
    # Get the current stock price
    test = input("Date of expiration (T) in 'YYYY-MM-DD' format: ")
    test1 = fonctions_option_pricing.number_of_days_to_expiration(test)
    print(f"Number of days until expiration: {test1} days")
    stock_data = yf.Ticker(chosen_stock)
    S = stock_data.history(period='1d')['Close'][0]

    # User input for option parameters
    K = float(input("Enter the strike price (K): "))
    T_days = fonctions_option_pricing.number_of_days_to_expiration(input("Enter the date of expiration (T) in 'YYYY-MM-DD' format: "))
    T = T_days / 365.0  # Convert days to years 
    r = float(input("Enter the risk-free interest rate (r) as a decimal: "))
    sigma = float(input("Enter the volatility of the stock (sigma) as a decimal: "))
    option_type = input("Enter the option type ('call' or 'put'): ").strip().lower()

    # Calculate the option price using the Black-Scholes formula
    option_price = fonctions_option_pricing.black_scholes_formula(S, K, T, r, sigma, option_type)
    
    print(f"The price of the {option_type} option is: {option_price:.2f}")
