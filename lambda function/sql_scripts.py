"import the required files"
import psycopg2 as db
from psycopg2 import extras
import boto3
import io
import pandas as pd

class SQL:
    """
    Class contains functions to save the data from s3 csv to
    database in AWS RDS.
    """
    
    def get_data(filename):
        """
        Function to get csv from s3 bucket

        Args:
            filename (string): filename.csv name of the file to get
        
        Returns:
            df(pandas dataframe): pandas dataframe of the csv requested
        """
        s3_file_key = 'stockData/' + filename
        bucket = 'my-stocks'
        
        #keys
        access = 'AKIAUUVNNLQM6OHYMFFL'
        secret = '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'
        #set the session
        session = boto3.Session(
            aws_access_key_id=access,
            aws_secret_access_key=secret,
            region_name='us-west-1'
        )
        #get the file
        s3 = session.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=s3_file_key)

        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        
        return df
    
    
    def get_connection():
        """
        Function to generate database connection with
        AWS RDS database.

        Returns:
            conn(postgres sql): connection to the database
        """
        conn = db.connect(
            database = "StockDB", 
            user = "onkar", 
            password = "onkar4996", 
            host = "stockdb.cfb7ftjb28h8.us-west-1.rds.amazonaws.com", 
            port = "5432")
        
        return conn
    
    
    def create_tables():
        """
        Function to create tables if not exist
        """
        #create accounts table
        acc_sql = """CREATE TABLE IF NOT EXISTS accounts
                    (
                        Date date NOT NULL,
                        AccReceivables bigint NOT NULL,
                        AccPayable bigint NOT NULL,
                        Company int NOT NULL
                    )"""
        #create earnings table
        earn_sql = """CREATE TABLE IF NOT EXISTS earnings
                        (
                            Year int NOT NULL,
                            Revenue bigint NOT NULL,
                            Earnings bigint NOT NULL,
                            Company int NOT NULL
                        )"""
        #create forecast table
        forecast_sql = """CREATE TABLE IF NOT EXISTS forecast
                        (
                            Date date NOT NULL,
                            Close real NOT NULL,
                            Company int NOT NULL
                        )"""
        #create performance table
        perf_sql = """CREATE TABLE IF NOT EXISTS performance
                        (
                            Date date NOT NULL,
                            Open double precision NOT NULL,
                            High double precision NOT NULL,
                            Low double precision NOT NULL,
                            Close double precision NOT NULL,
                            AdjClose double precision NOT NULL,
                            Volume bigint NOT NULL,
                            Company int NOT NULL,
                            pct_change double precision
                        )"""
        #create ratios table
        ratio_sql = """CREATE TABLE IF NOT EXISTS ratios
                    (
                        Date date NOT NULL,
                        CashRatio real NOT NULL,
                        QuickRatio real NOT NULL,
                        CurrRatio real NOT NULL,
                        LongTermDebtRatio real NOT NULL,
                        Company int NOT NULL
                    )"""
        
        sql_lst = [acc_sql, earn_sql, forecast_sql, perf_sql, ratio_sql]
        #get connection
        conn = SQL.get_connection()
        cur = conn.cursor()

        #loop through the tables
        for s in sql_lst:
            cur.execute(s)

        #commit
        conn.commit()
        #close the connection
        conn.close()
        
    
    def insert_accounts():
        """
        Function to insert the records from accounts.csv into the
        accounts table.
        """
        #get the connection
        conn = SQL.get_connection()
        cur = conn.cursor()
        #check if records exists
        get = "SELECT COUNT(*) FROM accounts"
        cur.execute(get)
        records = cur.fetchone()

        #if the record exists
        if records[0] == 0:
            #insert into the database
            df = SQL.get_data("accounts.csv")
            sql = """INSERT INTO accounts (Date, AccReceivables, AccPayable, Company) VALUES %s"""
            extras.execute_values(cur, sql, df.values)
            #commit
            conn.commit()

        conn.close()
        
        
    def insert_earnings():
        """
        Function to insert the records from earnings.csv into the
        earnings table.
        """
        #get the connection
        conn = SQL.get_connection()
        cur = conn.cursor()
        #check if records exists
        get = "SELECT COUNT(*) FROM earnings"
        cur.execute(get)
        records = cur.fetchone()

        #if the record exists
        if records[0] == 0:
            #insert into the database
            df = SQL.get_data("earnings.csv")
            sql = """INSERT INTO earnings (Year, Revenue, Earnings, Company) VALUES %s"""
            df = df.astype("float")
            tpls = [tuple(x) for x in df.to_numpy()]
            extras.execute_values(cur, sql, tpls)
            #commit
            conn.commit()

        #close the connection
        conn.close()
        
    
    def insert_ratios():
        """
        Function to insert the records from ratios.csv into the
        ratios table.
        """
        #get the connection
        conn = SQL.get_connection()
        cur = conn.cursor()
        #check if records exists
        get = "SELECT COUNT(*) FROM ratios"
        cur.execute(get)
        records = cur.fetchone()

        #if the record exists
        if records[0] == 0:
            #insert into the database
            df = SQL.get_data("ratios.csv")
            sql = """INSERT INTO ratios (Date, CashRatio, QuickRatio, CurrRatio, LongTermDebtRatio, Company) VALUES %s"""
            extras.execute_values(cur, sql, df.values)
            #commit
            conn.commit()

        #close the connection
        conn.close()
        
    
    def insert_forecast():
        """
        Function to insert the records from forecast.csv into the
        forecast table.
        """
        #get the connection
        conn = SQL.get_connection()
        cur = conn.cursor()
        #check if records exists
        get = "SELECT COUNT(*) FROM forecast"
        cur.execute(get)
        records = cur.fetchone()

        if records[0] == 0:
            #insert into the database
            df = SQL.get_data("forecast.csv")
            sql = """INSERT INTO forecast (Date, Close, Company) VALUES %s"""
            extras.execute_values(cur, sql, df.values)

        else:
            #clear the table
            sql = """TRUNCATE forecast"""
            cur.execute(sql)
            conn.commit()
            #insert into the database
            df = SQL.get_data("forecast.csv")
            sql = """INSERT INTO forecast (Date, Close, Company) VALUES %s"""
            extras.execute_values(cur, sql, df.values)
        
        #commit
        conn.commit()
        #close the connection
        conn.close()
        
    
    def insert_performance():
        """
        Function to insert the records from performance.csv into the
        performance table.
        """

        #get the connection
        conn = SQL.get_connection()
        cur = conn.cursor()
        #check if records exists
        get = "SELECT COUNT(*) FROM performance"
        cur.execute(get)
        records = cur.fetchone()

        if records[0] == 0:
            #insert into the database
            df = SQL.get_data("performance.csv")
            sql = """INSERT INTO performance (Date, Open, High, Low, Close, AdjClose, Volume, Company, pct_change) VALUES %s"""
            extras.execute_values(cur, sql, df.values)
        else:
            #clear the table
            sql = """TRUNCATE performance"""
            cur.execute(sql)
            conn.commit()
            df = SQL.get_data("performance.csv")
            sql = """INSERT INTO performance (Date, Open, High, Low, Close, AdjClose, Volume, Company, pct_change) VALUES %s"""
            extras.execute_values(cur, sql, df.values)

        #commit
        conn.commit()
        #close the connection
        conn.close()

    
    def main():
        """
        Function to call all other functions
        """
        SQL.create_tables()
        SQL.insert_accounts()
        SQL.insert_earnings()
        SQL.insert_forecast()
        SQL.insert_performance()
        SQL.insert_ratios()
        

