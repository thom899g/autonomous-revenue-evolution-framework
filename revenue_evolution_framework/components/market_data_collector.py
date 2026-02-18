import logging
from typing import Dict, Any
import requests

class MarketDataCollector:
    """
    A class to collect real-time market data from various sources.
    Implements singleton pattern for single instance usage.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.api_keys = {
                'alpha_vantage': 'YOUR_API_KEY',
                'fred': 'YOUR_API_KEY'
            }
            cls._instance.data_cache = {}
            return cls._instance
        else:
            return cls._instance

    def collect_data(self, source: str, symbol: str) -> Dict[str, Any]:
        """
        Fetches market data from the specified API source.
        
        Args:
            source (str): Name of the data provider (e.g., 'alpha_vantage', 'fred').
            symbol (str): Symbol for which data is to be collected (e.g., 'AAPL').
            
        Returns:
            Dict[str, Any]: Market data in dictionary format or None if failed.
        
        Raises:
            ValueError: If source is not supported.
            KeyError: If API key is missing.
        """
        try:
            api_key = self.api_keys[source]
            response = requests.get(
                f'https://api.{source}.com/v1/{symbol}',
                params={'apikey': api_key}
            )
            if response.status_code == 200:
                data = response.json()
                self.cache_data(source, symbol, data)
                return data
            else:
                logging.error(f"API request failed with status code {response.status_code}")
                return None
        except KeyError:
            logging.error(f"Missing API key for source: {source}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while collecting data: {str(e)}")
            return None

    def cache_data(self, source: str, symbol: str, data: Dict[str, Any]) -> None:
        """
        Caches collected market data for quick access.
        
        Args:
            source (str): Name of the data provider.
            symbol (str): Symbol of the asset.
            data (Dict[str, Any]): Market data to cache.
        """
        self.data_cache[f"{source}_{symbol}"] = data

    def get_data(self, key: str) -> Dict[str, Any]:
        """
        Retrieves cached market data by key.
        
        Args:
            key (str): Cache key in format "source_symbol".
            
        Returns:
            Dict[str, Any]: Cached data or None if not found.
        """
        return self.data_cache.get(key)