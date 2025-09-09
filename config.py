"""
Configuration settings for the All Bitcoin Private Key application
"""

# Number of addresses to display per page
ADDRESSES_PER_PAGE = 500

# Performance options
ENABLE_BALANCE_CHECKING = True  # Set to True for balance scanning functionality
MAX_SEARCH_PAGES = 1000  # Maximum pages to search through for address lookup (reduced for faster search)

# API configuration - Optimized for speed
API_REQUEST_DELAY = 0.05  # seconds between API requests (further reduced)
API_CHUNK_SIZE = 200      # addresses per API request (doubled for fewer requests)
API_MAX_THREADS = 10      # maximum concurrent threads (doubled for parallel processing)

# Bitcoin configuration
BITCOIN_MAX_NUMBER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140

# Flask configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True
