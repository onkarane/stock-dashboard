'import required files'
import pandas as pd
import yfinance as yf
import psycopg2 as db

class ChartHelper:
    
    """
    Class contains all the helper functions required
    for generating graphs.
    """
    
    def get_connection():
        """
        Function to generate database connection with
        AWS RDS database.

        Returns:
            conn(postgres sql): connection to the database
        """
        #form the connection to the database
        conn = db.connect(
            database = "", 
            user = "", 
            password = "", 
            host = "", 
            port = "")
        
        return conn
    
    def get_data(table_name):
        
        """
        Function to retrive the records from the database and return 
        a dataframe of the records.
        
        Args:
            table_name(string): name of the table to get the records from
        
        Returns:
            df(pandas dataframe): pandas dataframe of the table queried
        """
        #construct sql statement
        sql = "Select * from {f}".format(f = table_name)
        #get the column names
        if table_name == "accounts":
            cols = ['Date', 'AccReceivables', 'AccPayable', 'Company']
        elif table_name == "earnings":
            cols = ['Year', 'Revenue', 'Earnings', 'Company']
        elif table_name == "forecast":
            cols = ['Date', 'Close', 'Company']
        elif table_name == "performance":
            cols = ['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume', 'Company', 'pct_change']
        elif table_name == "ratios":
            cols = ['Date', 'CashRatio', 'QuickRatio', 'CurrRatio', 'LongTermDebtRatio', 'Company']

        #get the connection
        conn = ChartHelper.get_connection()
        cur = conn.cursor()
        #get the records
        cur.execute(sql)
        data = cur.fetchall()

        #make dataframe
        df = pd.DataFrame(data, columns=cols)
        #close the connection
        conn.close()

        return df

    
    def get_symbol(company):
        """
        Function to get company symbol based on the 
        id provided.

        Args:
            company(string): Id number of the company
            
        Returns:
            symbol(string): name of the stock
        """
        #dict for mapping company id to name 
        comp = {
            0: "MSFT",
            1: "TSLA",
            2: "AMZN",
            3: "AAPL",
            4: "GOOG"
        }
        symbol = comp[company]
        
        return symbol
    
    def get_current_price(company):
        """
        Function to get and return current
        stock price of given company.

        Args:
            company(string): Id number of the company
            
        Returns:
            todays_data(float): Current price of the stock
        """
        #get the symbol
        symbol = ChartHelper.get_symbol(company)
        
        #get the price
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        todays_data = todays_data['Close'][0]
        
        return round(todays_data, 2)
