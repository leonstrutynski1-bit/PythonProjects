# The fonctions used in my option pricing code
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import norm


def black_scholes_formula(S, K, T, r, sigma, option_type='call'):
    """
    Calculate the Black-Scholes option price.

    Parameters:
    S (float): Current stock price
    K (float): Strike price
    T (float): Time to maturity in years
    r (float): Risk-free interest rate
    sigma (float): Volatility of the stock
    option_type (str): 'call' for call option, 'put' for put option

    Returns:
    float: Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return option_price


def number_of_days_to_expiration(expiration_date):
    """
    Calculate the number of days until the option expires.

    Parameters:
    expiration_date (str): Expiration date in 'YYYY-MM-DD' format

    Returns:
    int: Number of days until expiration
    """
    today = pd.Timestamp.today().normalize()
    expiration = pd.Timestamp(expiration_date)
    return (expiration - today).days