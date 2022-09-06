from datetime import date
import yfinance as yf
import numpy as np
import pandas as pd


# Gather user input: ticker symbols and asset weights
num_stocks = int(input("How many stocks in your portfolio? "))

tickers = []
for i in range(num_stocks):
    stock = input("Enter stock " + str(i + 1) +": ")
    tickers.append(stock)

weights = []
for i in range(num_stocks):
    weight = input("Enter weight for stock " + str(i + 1) +": ")
    weights.append(weight)

portf_dict = {}
count = 0 
for stock in tickers:
    portf_dict[stock] = weights[count]
    count += 1

print(portf_dict)

start = date(2014, 1, 1)
end = date(2021, 12, 31)

stockdata = yf.download(tickers, start, end)['Adj Close']

# STANDARD DEVIATION
#   First get the % daily change for each ticker. 
#   Then multiply each % change by natural log to account for compounding effects
#   Find daily standard deviation with .std()
#   Annualize by multiplying by sqrt(250), assuming 250 trading days on average
pctchng_stockdata = stockdata.pct_change().apply(lambda x: np.log(1+x))
std_stockdata = pctchng_stockdata.std().apply(lambda x: x*np.sqrt(250))

# COVARIANCE MATRIX
cov_matrix = pctchng_stockdata.cov()

# EXPECTED RETURN (Using ANNUAL returns)
annual_stockdata = stockdata.resample('Y').last().pct_change()
exp_ret = annual_stockdata.mean()

# Concatenate into one dataframe
assets = pd.concat([exp_ret, std_stockdata], axis=1)
assets.columns = ['Returns', 'STDev']

# Instantiate empty lists for portfolio data
#   Need ORDERED_WEIGHTS because stockdata is in alphabetical order, whereas user input is not necessarily in alph order
portf_ret = []
portf_std = []
ordered_weights = []
portf_weights = []

# Number of assets in our portfolio
num_assets = len(stockdata.columns)

# Potential for more than one portfolio with different weights
num_portfolios = 1

for portfolio in range(num_portfolios):

    # Make sure each user-inputed asset weight corresponds to the correct stock
    for stock in stockdata.columns:
        ordered_weights.append(float(portf_dict[stock]))
    
    portf_weights.append(ordered_weights) # Append the given weights to our portfolio data

    returns = np.dot(ordered_weights, exp_ret) # E[x] of portfolio is a dot product of the weights and E[x] of each stock
    portf_ret.append(returns) # Append results to our portfolio data

    var = cov_matrix.mul(ordered_weights, axis=0).mul(ordered_weights, axis=1).sum().sum() # Covariance matrix 

    sd = np.sqrt(var)*np.sqrt(250) # Standard deviation part of the formula, annualized
    portf_std.append(sd) # Append results to our portfolio data

# Create the dataframe for the portfolio using a dictionary
data = {'Returns':portf_ret, 'STDev':portf_std}
portfolios = pd.DataFrame(data)

# Concatenate the individual stock E[x] and SD to the portfolio E[x] and SD so everything is visible at once
portfolios.index = ['Portfolio']
portfolio_assets = pd.concat([portfolios, assets])

print(portfolio_assets)

# Sharpe Ratio calculation
RISK_FREE = 0.032
sr = (portfolios['Returns'] - RISK_FREE) / portfolios['STDev']
print('Sharpe Ratio: ' + str(sr))

# portfolio_assets.plot.scatter(x='STDev', y='Returns', grid=True)
