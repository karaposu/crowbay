import requests
import datetime

class CMCPriceFetcher:
    def __init__(self, api_key):
        """
        Initializes the price fetcher with your CoinMarketCap Pro API key.
        
        :param api_key: Your CoinMarketCap Pro API key as a string
        """
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com"
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }
     
    def get_latest_price_info(self, symbol, convert="USD"):
        """
        Retrieves the latest price quote for a given symbol.
        
        :param symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        :param convert: The fiat or crypto currency to convert the price into (default: 'USD')
        :return: A dictionary containing the latest price info returned by CMC.
        """
        # For details, see: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest
        params = {
            "symbol": symbol,
            "convert": convert
        }
        
        url = f"{self.base_url}/v1/cryptocurrency/quotes/latest"
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"Failed to fetch latest price info: {response.status_code} - {response.text}"
            )

    
    def get_last_year_price_history(self, symbol):
        """
        Retrieves the daily historical data for the past 1 year for the given symbol.
        
        :param symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        :return: A dictionary with CoinMarketCap's response containing OHLCV daily data.
        """
        # Calculate the start and end times (1 year ago to now) in UTC
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=365)
        
        # Create parameters for the API request
        # For more details on parameter usage, see:
        # https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyOhlcvHistorical
        params = {
            "symbol": symbol,
            "time_start": start_time.isoformat(),  # ISO8601 format
            "time_end": end_time.isoformat(),
            "interval": "daily",
        }
        
        # Construct the request URL
        url = f"{self.base_url}/v1/cryptocurrency/ohlcv/historical"
        
        # Make the request
        response = requests.get(url, headers=self.headers, params=params)
        
        # If the response is successful, parse it as JSON
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            # If not successful, raise an exception with the error message
            raise Exception(
                f"Failed to fetch historical data: {response.status_code} - {response.text}"
            )

# ------------------------
# Example Usage:
# ------------------------
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
    # Replace 'YOUR_API_KEY' with your actual CoinMarketCap Pro API key
    cmc_fetcher = CMCPriceFetcher(api_key="COINMARKETCAP_API_KEY")
    
    # Fetch 1-year daily historical data for Bitcoin (BTC)
    try:
        btc_history = cmc_fetcher.get_last_year_price_history("BTC")
        print("BTC 1-year history:")
        print(btc_history)
    except Exception as e:
        print(e)



