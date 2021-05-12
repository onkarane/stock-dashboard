import boto3
import pandas as pd
from prophet import Prophet
from datetime import date
from io import StringIO
import io

class Predictions:
    
    """
    Contains all the functions to generate
    predictions and save it to aws cloud.
    """
    
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
    
    
    def process_dataframe(df):
        """
        Function to convert the dataframe into fbprophet format.

        Args:
            df (pandas dataframe): pandas dataframe with date and target column

        Returns:
            df(pandas dataframe): pandas dataframe with ds for date and y 
            for target column value
        """
        #filter dataframe
        df = df[['Date', 'Close']]
        #convert date col into datetime format
        #rename the columns
        cols = {'Date': 'ds', 'Close': 'y'}
        df = df.rename(columns = cols)
        
        return df
    
    
    def generate_predictions(df):
        """
        Function to generate the model and predict the stock prices

        Args:
            df(pandas dataframe): pandas dataframe with ds for date and y 
            for target column value

        Returns:
            forecast(pandas dataframe): pandas dataframe with Date, Close values
            for next three months.
        """
        #generate model
        m = Prophet(daily_seasonality=True, changepoint_prior_scale=0.15)
        m.fit(df)
        #generate future dates
        future = m.make_future_dataframe(periods=90)

        #predictions
        forecast = m.predict(future)
        #filter the predictions
        forecast = forecast[['ds', 'yhat']]
        #rename the columns
        cols = {'ds': 'Date', 'yhat': 'Close'}
        forecast = forecast.rename(columns = cols)

        #filter the dates
        today = date.today().strftime("%Y-%m-%d")
        forecast = forecast[forecast['Date'] > today]
        #reset index
        
        return forecast
    

    def main():
        """
        Main function to call all other functions
        """
        #get the data
        data = Predictions.get_data('performance.csv')
        #empty dataframe and list
        pred = pd.DataFrame()
        df_list = []
        #company id list
        id_list = [0, 1, 2, 3, 4]

        for i in id_list:
            #filter company
            df = data[data['Company'] == i]
            #process the dataframe
            df = Predictions.process_dataframe(df)
            #get the predictions
            df = Predictions.generate_predictions(df)
            df['Company'] = i
            #append
            df_list.append(df)

        #make final dataframe
        for i in range(len(df_list)):
            pred = pred.append(df_list[i])
        #reset index
        pred = pred.reset_index().drop(columns='index', axis=1)
        #round the values
        pred['Close'] = pred['Close'].round(2)
        #set the index
        pred = pred.set_index('Date')
        #filter out weekends
        pred = pred[pred.index.dayofweek < 5]
        
        
        #save the dataframe
        Predictions.save_data(pred, 'forecast.csv')


    