"""This is for all the code used to interact with the AlphaVantage API
and the SQLite database. Remember that the API relies on a key that is
stored in the `.env` file and imported via the `config` module.
"""

import sqlite3
import pandas as pd
import requests
from config import settings    

class AlphaVantageAPI:
    def __init__(self, api_key=settings.alpha_vantage_api_key):
        self.__api_key = api_key  # Just a way to make it a secret attribute, you can access it but won't appear when you do dir

    def get_daily(self, ticker, output_size="full", data_type="json"):
        self.ticker = ticker
        self.output_size = output_size
        self.data_type = data_type

        url = f"https://www.alphavantage.co/query?" \
              f"function=TIME_SERIES_DAILY&" \
              f"symbol={self.ticker}&" \
              f"outputsize={self.output_size}&" \
              f"datatype={self.data_type}&" \
              f"apikey={self.__api_key}"

        # Send request to API
        response = requests.get(url=url)

        # Check for successful response
        if response.status_code != 200:
            raise Exception(
                f"Invalid API call. Check if the ticker symbol '{ticker}' is correct"
            )

        # Extract JSON data from response
        response_data = response.json()

        if 'Time Series (Daily)' not in response_data:
            raise Exception(
                f"Invalid API call. Check if the ticker symbol '{ticker}' is correct"
            )

        stock_data = response_data['Time Series (Daily)']

        # Read data into DataFrame
        df = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)

        # Convert index to `DatetimeIndex` named "Date"
        df.index = pd.to_datetime(df.index)

        # Let's give our index name
        df.index.name = "Date"

        # Remove numbering from columns
        df.columns = [col.split(" ")[1] for col in df.columns]

        # Return DataFrame
        return df



class SQLRepository:
    def __init__(self, connection):
        self.connection = connection

    def insert_table(self, table_name, records, if_exists="fail"):
    
        """Insert DataFrame into SQLite database as table

        Parameters
        ----------
        table_name : str
        records : pd.DataFrame
        if_exists : str, optional
            How to behave if the table already exists.

            - 'fail': Raise a ValueError.
            - 'replace': Drop the table before inserting new values.
            - 'append': Insert new values to the existing table.

            Dafault: 'fail'

        Returns
        -------
        dict
            Dictionary has two keys:

            - 'transaction_successful', followed by bool
            - 'records_inserted', followed by int
        """
        n_inserted = records.to_sql(name=table_name, 
                            con=self.connection, if_exists=if_exists)
        return {
            "transactional_successful": True,
            "record_inserted": n_inserted
        }
        
        

    def read_table(self, table_name, limit=None):
    
        """Read table from database.

        Parameters
        ----------
        table_name : str
            Name of table in SQLite database.
        limit : int, None, optional
            Number of most recent records to retrieve. If `None`, all
            records are retrieved. By default, `None`.

        Returns
        -------
        pd.DataFrame
            Index is DatetimeIndex "date". Columns are 'open', 'high',
            'low', 'close', and 'volume'. All columns are numeric.
        """
        # Create SQL query (with optional limit)
        if limit:
            query = f"SELECT FROM {table_name} LIMIT {limit}"
        else:
            query = f"SELECT FRON {table_name}"
        

        # Retrieve data, read into DataFrame
        df = pd.read_sql(sql=query, con=self.connection, parse_dates = ["Date"])
        df.set_index("Date", inplace=True)
        # Return DataFrame
        return df
