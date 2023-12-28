"""
Code to extract any of the STOCK we are trying to applying machine learning for prediction
"""

from config import settings
import pandas as pd
import requests

# Function to extract url from AlphaVantage
def alphavantage_url(ticker : str, output_size : str, data_type : str):
    base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"
    url = (base_url + f"symbol={ticker}&" + 
                f"outputsize={output_size}&" + f"datatype={data_type}&" +
                     f"apikey={settings.alpha_vantage_api_key}")  
    return url 


# Function to make request fron the url and convert into Pandas DataFrame
def request_and_convert_to_dataframe(url):
    response = requests.get(url=url)
    print(f"response for the code is {response.status_code}")
    response_data  = response.json()
    if 'Time Series (Daily)' not in response_data.keys():
        raise Exception(
            f"Invalid API call. Check if the ticker symbol is correct"
        )
    stock_data = response_data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)
    # Converting the Date from string, to Date time index
    df.index = pd.to_datetime(df.index)
    # Lets give our index name 
    df.index.name = "Date"
    df.columns = [col.split(" ")[1] for col in df.columns]
    return df


   # OR 
def get_daily(ticker : str, output_size : str, data_type : str):

    """Get daily time series of an equity from AlphaVantage API.

    Parameters
    ----------
    ticker : str
        The ticker symbol of the equity.
    output_size : str, optional
        Number of observations to retrieve. "compact" returns the
        latest 100 observations. "full" returns all observations for
        equity. By default "full".
    data_type : str, optional
        

    Returns
    -------
    pd.DataFrame
        Columns are 'open', 'high', 'low', 'close', and 'volume'.
        All are numeric.
    """
    
    url = ("https://www.alphavantage.co/query?"
       "function=TIME_SERIES_DAILY&"
       f"symbol={ticker}&"
       f"outputsize={output_size}&"
       f"datatype={data_type}&"
       f"apikey={settings.alpha_vantage_api_key}"
    )

    # Send request to API 
    response = requests.ger(url = url)

    # Extract JSON data from response 
    response_data = response.json()
    if 'Time Series (Daily)' not in response_data.keys():
        raise Exception(
            f"Invalid API call. Check if the ticker symbol '{ticker}' is correct"
        )

    stock_data = response_data['Time Series (Daily)']
    
    # Read data into DataFrame 
    df = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)

    # Convert index to `DatetimeIndex` named "Date" 
    df.index = pd.to_datetime(df.index)

    # Lets give our index name 
    df.index.name = "Date"

    # Remove numbering from columns 
    df.columns = [col.split(" ")[1] for col in df.columns]

    # Return DataFrame
    return df