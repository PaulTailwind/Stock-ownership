# Stock ownership calculator
import yfinance as yf
from datetime import datetime

# Stock ownership class using stock price information from Yahoo Finance   
class ownership_calculator:
    
    """
    The class calculates the value and the return of a hypothetical investment in one of the tech stocks at IPO.
    The share price and stock split information is pulled from Yahoo! Finance using the yfinance library. 
    More information on yfinance: https://pypi.org/project/yfinance/
    
    The class currently supports four stocks: AAPL, AMZN, NFLX, MSFT
    The date and the price at IPO are hard inputs from the following sources:
        AAPL: https://investor.apple.com/faq/default.aspx
        AMZN: https://markets.businessinsider.com/stocks/amzn-stock
        NFLX: https://money.cnn.com/2002/05/23/markets/ipo/ipos/index.htm
        MSFT: https://news.microsoft.com/announcement/microsoft-goes-public/
    
    Calculation logic:
        [1] Number of stocks bought at IPO: investment // stock price at IPO
        [2] Number of stocks after splits: [1] * stock split mutltiple
        [3] Value of stocks today: [2] * today's stock price
        [4] Total return: [3] / investment - 1
        [5] Annual return: ([3] / investment)**(1/years from IPO) - 1
        
    Input: ticker, investment amount
    Output:
        get_investment_worth - investment worth today taking into account stock splits
        get_roi - total return on the investment
        get_aroi - annualized total return on the investment
        get_summary - summary string
    """
    
    def __init__(self, ticker, investment):
        
        self.IPO_DATA = {
            "AAPL":{"Name":"Apple", "Date":"12-12-1980", "Price":22.00},
            "AMZN":{"Name":"Amazon", "Date":"05-15-1997", "Price":18.00},
            "NFLX":{"Name":"Netflix", "Date":"05-23-2001", "Price":15.00},
            "MSFT":{"Name":"Microsoft", "Date":"03-13-1986", "Price":21.00}
        }
        
        # Supported stock tickers
        assert ticker in self.IPO_DATA, "{0} is not supported".format(ticker)
        # Positive investment
        assert investment > 0, "Investment should be > 0"
        
        self.company = self.IPO_DATA[ticker]["Name"]
        self.stock = yf.Ticker(ticker)
        self.investment = float(investment)
        self.date_ipo = datetime.strptime(self.IPO_DATA[ticker]["Date"], "%m-%d-%Y")
        self.price_ipo = float(self.IPO_DATA[ticker]["Price"])
        self.stock_number_ipo = int(self.investment // self.price_ipo)
        self.stock_splits_adj = self.stock.splits.product()
        self.__prices = self.stock.history(period="1d")
        self.price_today = float(self.__prices['Close'][0])
        self.worth_today = self.stock_number_ipo * self.stock_splits_adj * self.price_today
        self.roi = self.worth_today / self.investment - 1
        self.investment_period = (datetime.now() - self.date_ipo).days / 365
        self.aroi = (self.worth_today / self.investment)**(1/self.investment_period) - 1
        self.summary = 'If you would have invested ${0:,g} in {1} at its IPO in {2}, your investment would be worth ${3:,g} today, resulting in a total return on investment of {4:,.0%} or {5:.02%} per annum.'.format(self.investment, self.company, self.date_ipo.year, self.worth_today, self.roi, self.aroi)
        
    # Investment worth today
    def get_investment_worth(self):
        return self.worth_today
    
    # Total return on investment
    def get_roi(self):
        return self.roi
    
    # Annualized total return on investment
    def get_aroi(self):
        return self.aroi
    
    # Conclusion string
    def get_summary(self):
        return self.summary

# Test
if __name__ == "__main__":
    oc = ownership_calculator("AAPL", 500)
    print(oc.get_summary())
    