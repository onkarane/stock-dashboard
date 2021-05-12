'import required files'
from stocks import Stocks
import requests
import psycopg2 as db
from sql import SQL

def lambda_handler(event, context):
    # call the main function to process data
    Stocks.main()
    #Call the heroku model to process forecast
    url = "https://forecast-prophet.herokuapp.com/?message=pred"
    reponse = requests.get(url)
    #print(reponse)
    SQL.main()
    
    

