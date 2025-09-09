"""
Configuration settings for the All Bitcoin Private Key application
"""

# Number of addresses to display per page
ADDRESSES_PER_PAGE = 500

# Performance options
ENABLE_BALANCE_CHECKING = True  # Set to True for balance scanning functionality
MAX_SEARCH_PAGES = 100   # Maximum pages to search through for address lookup (reduced for Vercel)

# API configuration - Optimized for Vercel serverless
API_REQUEST_DELAY = 0.1   # seconds between API requests (increased for Vercel stability)
API_CHUNK_SIZE = 100      # addresses per API request (reduced for Vercel)
API_MAX_THREADS = 3       # maximum concurrent threads (reduced for Vercel)

# Bitcoin configuration
BITCOIN_MAX_NUMBER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140

# Flask configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True  # Set to True for development (auto-reload templates)
