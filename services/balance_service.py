import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from models.blockchain import Blockchain
from config import API_REQUEST_DELAY, API_CHUNK_SIZE, API_MAX_THREADS

class BalanceService:
    """Service for fetching Bitcoin balance information from blockchain.info"""
    
    def __init__(self):
        self.base_url = "https://blockchain.info/balance"
        self.request_delay = API_REQUEST_DELAY
        self.max_threads = API_MAX_THREADS
        self._cache = {}  # Simple in-memory cache
        self._cache_lock = threading.Lock()
    
    def get_balance(self, addresses: List[str]) -> Dict[str, Blockchain]:
        """Fetch balance information for multiple addresses using concurrent requests and caching"""
        if not addresses:
            return {}
        
        # Check cache first
        all_balances = {}
        uncached_addresses = []
        
        with self._cache_lock:
            for address in addresses:
                if address in self._cache:
                    all_balances[address] = self._cache[address]
                else:
                    uncached_addresses.append(address)
        
        # If all addresses are cached, return immediately
        if not uncached_addresses:
            return all_balances
        
        # Fetch uncached addresses
        chunk_size = API_CHUNK_SIZE
        chunks = [uncached_addresses[i:i + chunk_size] for i in range(0, len(uncached_addresses), chunk_size)]
        
        # Use ThreadPoolExecutor for concurrent API requests
        with ThreadPoolExecutor(max_workers=API_MAX_THREADS) as executor:
            # Submit all chunk requests concurrently
            future_to_chunk = {
                executor.submit(self._fetch_balance_chunk, chunk): chunk 
                for chunk in chunks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_chunk):
                try:
                    chunk_balances = future.result()
                    all_balances.update(chunk_balances)
                    
                    # Cache the results
                    with self._cache_lock:
                        self._cache.update(chunk_balances)
                        
                except Exception as e:
                    print(f"Error fetching balance chunk: {e}")
                    # Continue with other chunks even if one fails
        
        return all_balances
    
    def _fetch_balance_chunk(self, addresses: List[str]) -> Dict[str, Blockchain]:
        """Fetch balance for a chunk of addresses"""
        try:
            # Prepare the request URL
            addresses_str = ','.join(addresses)
            url = f"{self.base_url}?cors=true&active={addresses_str}"
            
            # Make the request
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Convert to our Blockchain objects
            balances = {}
            for address, balance_data in data.items():
                balances[address] = Blockchain(
                    final_balance=balance_data.get('final_balance', 0),
                    n_tx=balance_data.get('n_tx', 0),
                    total_received=balance_data.get('total_received', 0)
                )
            
            return balances
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching balance data: {e}")
            print(f"URL attempted: {url}")
            print(f"Addresses: {addresses[:3]}...")  # Show first 3 addresses
            # Return empty balances for this chunk
            return {address: Blockchain(0, 0, 0) for address in addresses}
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"URL attempted: {url}")
            print(f"Addresses: {addresses[:3]}...")  # Show first 3 addresses
            return {address: Blockchain(0, 0, 0) for address in addresses}
