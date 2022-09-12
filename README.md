# Project Summary
This Python web-app calculates expected return, standard deviation, and sharpe ratio of a portfolio of public assets inputed by the user. The portfolio can be any number of assets and the ticker symbols of the stocks must be listed on Yahoo Finance. 
# Libraries Used
- [yfinance](https://pypi.org/project/yfinance/) - Used to scrape Yahoo Finance historical price data.
- [Pandas](https://pandas.pydata.org/) - Used for higher level data analysis. 
# Goals of the Project and Why it is Useful
When building a portfolio of stocks, it is undesirable take on risk without any compensation. In other words, we want the best possible Sharpe Ratio for our portfolio. Brokers typically do not have any features that inform the user of the expected return and standard deviation of their portfolio. With this app, simply input the tickers of your assets and corresponding weights to see the Sharpe Ratio of your portfolio. You might discover that you can earn the same expected return for a lower standard deviation by rebalancing your portfolio or adding more stocks.