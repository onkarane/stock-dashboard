'import required files'
#libraries for aws
import boto3
from io import StringIO
#date functions
from datetime import date
from dateutil.relativedelta import relativedelta
#stock manipulation
import yfinance as yf
import pandas as pd

class Stocks:
    
    """
    Class contains helper functions to update the data files.
    """
    
    def calculate_dates():
        """
        Function to calculate todays date and
        previous date 3 months from now
        
        Returns:
            today(string): date in %Y-%m-%d format
            previous(string): date in %Y-%m-%d format
        """
        #get todays date
        today = date.today().strftime("%Y-%m-%d")
        #date from 3 months ago
        previous = date.today() + relativedelta(months=-3)
        previous = previous.strftime("%Y-%m-%d")
        
        return today, previous
    
    
    def save_data(df, filename):
        """
        Function to save files to aws s3 as csv.
        
        Args:
            df(pandas datafrmae): dataframe to be saved to s3
            filename(string): filename.csv for the dataframe to be saved to s3
        """
        #keys
        access = 'AKIAUUVNNLQM6OHYMFFL'
        secret = '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'
        #set the session
        session = boto3.Session(
            aws_access_key_id=access,
            aws_secret_access_key=secret,
            region_name='us-west-1'
        )
        #set resource
        s3 = session.resource('s3')
        #bucket-name
        bucket = 'my-stocks'
        #create buffer
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        #save the file
        path = 'stockData/' + filename
        s3.Object(bucket, path).put(Body=csv_buffer.getvalue())
        
    
    def map_companies(df):
        """
        Function to map the company names to
        their respective company ids.

        Args:
            df (pandas dataframe): pandas dataframe with company names column
        
        Returns:
            df (pandas dataframe): pandas dataframe with mapped company names
        """
        #define dictionary to map
        company = {
            "MSFT": 0,
            "TSLA": 1,
            "AMZN": 2,
            "AAPL": 3,
            "GOOG": 4
        }
        #map the companies
        df['Company'] = df['Company'].map(company)
        
        return df
    
    def get_performance_data():
        """
        Function to get the performance data
        for past 3 months from todays date.
        """
        #set the list
        companies = ['MSFT', 'TSLA', 'AMZN', 'AAPL', 'GOOG']
        #set an empty dataframe
        df = pd.DataFrame()
        #list for data
        lst = []
        
        #get the dates
        today, previous = Stocks.calculate_dates()
        
        #loop through the list
        for c in companies:
            data = yf.download(c, start=previous, end=today)
            #append company name
            data['Company'] = c
            #calculate percent change
            data['pct_change'] = data['Close'].pct_change()
            lst.append(data)
        
        #make final dataframe
        for i in range(len(lst)):
            df = df.append(lst[i])
        #map the company names
        df = Stocks.map_companies(df)
            
        #save the dataframe
        Stocks.save_data(df, 'performance.csv')
    
    def get_earnings_data():
        """
        Function to earnings and revenue data for the
        companies.
        """
        #set the list
        companies = ['MSFT','TSLA', 'AMZN', 'AAPL', 'GOOG']
        #set an empty dataframe
        df = pd.DataFrame()
        #list of data
        lst = []
        
        #loop through the companies
        for c in companies:
            tick = yf.Ticker(c)
            #get the data
            data = tick.earnings
            data['Company'] = c
            
            #append to the list
            lst.append(data)
        
        #make final dataframe
        for i in range(len(lst)):
            df = df.append(lst[i])
        #map the company names
        df = Stocks.map_companies(df)
            
        #save the dataframe
        Stocks.save_data(df, 'earnings.csv')
        
    
    def get_balance_sheet_data():
        """
        Function to create balance sheet ratios such as
        Cash Ratio, Current Ratio, Quick Ratio etc.
        """
        #set the list
        companies = ['MSFT','TSLA', 'AMZN', 'AAPL', 'GOOG']
        #set an empty dataframe
        df = pd.DataFrame()
        #list
        lst = []
        
        #loop through the companies
        for c in companies:
            temp_df = pd.DataFrame()
            #set the ticket
            tick = yf.Ticker(c)
            #get the balance sheet data and Tranpose
            data = tick.balance_sheet
            dt = data.T
        
            #perform the calculations for ratios
            if c == 'TSLA':
                temp_df['CashRatio'] = (dt['Cash'] + 0) / dt['Total Current Liabilities']
                temp_df['QuickRatio'] = (dt['Cash'] + dt['Net Receivables'] + 0) / dt['Total Current Liabilities']
            else:
                temp_df['CashRatio'] = (dt['Cash'] + dt['Short Term Investments']) / dt['Total Current Liabilities']
                temp_df['QuickRatio'] = (dt['Cash'] + dt['Net Receivables'] + dt['Short Term Investments']) / dt['Total Current Liabilities']
                
            temp_df['CurrRatio'] = dt['Total Current Assets'] / dt['Total Current Liabilities']
            temp_df['LongTermDebtRatio'] = dt['Long Term Debt'] / dt['Total Stockholder Equity']
            temp_df['Company'] = c
            #append to list
            lst.append(temp_df)
        
        #make final dataframe
        for i in range(len(lst)):
            df = df.append(lst[i])
        #name the index
        df.index.name = 'Date'
        
        #map the company names
        df = Stocks.map_companies(df)
        #round the values
        df = df.round(3)
        
        #save the dataframe
        Stocks.save_data(df, 'ratios.csv')
        
    
    def get_accounts_data():
        """
        Function to get accounts payable and accounts
        receiveable data.
        """
        #set the list
        companies = ['MSFT','TSLA', 'AMZN', 'AAPL', 'GOOG']
        #set an empty dataframe
        df = pd.DataFrame()
        #list of data
        lst = []
        
        #loop through the companies
        for c in companies:
            #temporary dataframe
            temp_df = pd.DataFrame()
            tick = yf.Ticker(c)
            #get the data
            data = tick.balance_sheet
            #transpose and get the required data
            data = data.T[['Net Receivables', 'Accounts Payable']]
            
            #set the dataframe
            temp_df['AccReceivables'] = data['Net Receivables']
            temp_df['AccPayable'] = data['Accounts Payable']
            temp_df['Company'] = c
            #add the temp dataframe to list
            lst.append(temp_df)
        
        #make final dataframe
        for i in range(len(lst)):
            df = df.append(lst[i])
        #map the company names
        df = Stocks.map_companies(df)
        #rename index
        df.index.name = 'Date'
        
        #save the dataframe
        Stocks.save_data(df, 'accounts.csv')
    
    
    def main():
        """
        Main function to call all other functions.
        """
        Stocks.get_performance_data()
        Stocks.get_accounts_data()
        Stocks.get_balance_sheet_data()
        Stocks.get_earnings_data()
