# PythonProjects — Finance & Quantitative Analysis

This repository contains a collection of my Python projects focused on finance, data analysis, and quantitative investing. These projects are part of my learning process as I develop practical programming and financial modeling skills alongside my studies.

## Main projects in this repository

### Stock Screener (Value-Based Strategy)
A Python-based stock screener that:
- Retrieves market and financial data using **yfinance**  
- Computes financial ratios (e.g., Trailing P/E, Book-to-Price)  
- Compares a chosen stock against a sample universe of 15 major Nasdaq tech companies  
- Implements a **Value Score inspired by the Fama–French HML factor**  
- Classifies stocks into **Buy / Hold / Sell** lists based on valuation  
- Includes visualization of price performance relative to a benchmark (QQQ)

> Note: This is a simplified, educational model and has not yet been fully backtested.

### Quantitative & Financial Modeling (Work in Progress)
Future improvements and ongoing work include:
- Adding a momentum filter to the value strategy  
- Backtesting strategies on historical data  

### Option Pricing Model (Planned Work)
This project will include:
- Implementing the Black–Scholes model to price European call and put options  
- Retrieving and preprocessing the required market inputs (spot price, volatility, interest rate, time to maturity)

## Tools & Libraries Used
- Python  
- Pandas, NumPy  
- yfinance  
- Matplotlib  
