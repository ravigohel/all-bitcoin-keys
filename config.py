"""
Configuration settings for the All Bitcoin Private Key application
"""

# Number of addresses to display per page
ADDRESSES_PER_PAGE = 500

# Performance options
ENABLE_BALANCE_CHECKING = True  # Set to False for maximum speed (no API calls)
MAX_SEARCH_PAGES = 2500  # Maximum pages to search through for address lookup

# API configuration
API_REQUEST_DELAY = 0.1  # seconds between API requests (reduced for speed)
API_CHUNK_SIZE = 100     # addresses per API request (increased for fewer requests)
API_MAX_THREADS = 5      # maximum concurrent threads (increased for parallel processing)

# Bitcoin configuration
BITCOIN_MAX_NUMBER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140

# Flask configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True
