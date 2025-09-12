# All Bitcoin Private Key - Python Version

A high-performance Python Flask application that generates Bitcoin private keys sequentially and displays their corresponding addresses with real-time balance information. This is a complete conversion of the original Angular TypeScript application with enhanced features and optimizations.

## 🚀 Key Features

### Core Functionality
- **Sequential Key Generation**: Generates Bitcoin private keys starting from 1 (0x000...001)
- **Dual Address Format**: Both compressed and uncompressed P2PKH addresses
- **Real-time Balance Checking**: Live balance data from blockchain.info API
- **Smart Address Search**: Find any Bitcoin address and its page location
- **Balance Discovery**: High-speed multi-page scanning for addresses with balances
- **Enhanced Navigation**: First, Previous, Random, Next, Last buttons for easy browsing
- **Page Percentage Display**: Shows current position with 2 decimal precision
- **Scientific Notation Pagination**: Display page numbers in scientific format (2.32×10⁷⁴)
- **Pagination**: Browse through 500 addresses per page with intuitive navigation

### User Experience
- **Intuitive Menu Names**: Browse Keys, Find Address, Find Balances, Info
- **Truncated Display**: Clean view showing first 7 and last 9 characters
- **Scientific Notation**: Professional display of page numbers (2.32×10⁷⁴ format)
- **Copy Functionality**: One-click copy buttons for full private keys and addresses
- **Page Totals**: Real-time total balance and received amounts in navigation bar
- **Green Balance Highlighting**: Non-zero balances highlighted in dark green
- **Random Page Access**: Jump to random pages for exploration
- **Responsive Design**: Modern, mobile-friendly interface

### Performance Optimizations
- **Concurrent API Requests**: 10 threads for faster balance checking
- **Batch Processing**: Single API call for multiple pages (10x faster)
- **Intelligent Caching**: In-memory cache for instant repeated requests
- **Configurable Settings**: Balance checking can be disabled for maximum speed
- **Optimized Chunking**: 200 addresses per API request for efficiency

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ravigohel/all-bitcoin-keys.git
cd all-bitcoin-keys
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
# OR use the startup script:
python run.py
```

4. **Open your browser:**
```
http://localhost:5000
```

## 🎯 Usage Guide

### Main Features
- **Browse Keys**: Navigate through pages using enhanced navigation (First, Previous, Random, Next, Last)
- **Find Address**: Search for specific Bitcoin addresses and get their page locations
- **Find Balances**: Scan multiple pages to discover addresses with actual Bitcoin balances
- **Copy Keys**: Click the 📋 button next to any private key or address to copy it
- **View Balances**: See real-time balance information with green highlighting
- **Page Totals**: Check total balance and received amounts for each page in the navigation bar
- **Page Percentage**: See your current position within the massive key space

### Quick Start
1. **Browse Keys**: Navigate through Bitcoin keys and addresses with enhanced controls
2. **Find Address**: Search for specific addresses and their page locations
3. **Find Balances**: Scan multiple pages for addresses with balances
4. **Info**: Learn about the application features and technical details

### Enhanced Navigation
- **First**: Jump to page 1
- **Previous**: Go to the previous page
- **Random**: Jump to a random page for exploration
- **Next**: Go to the next page
- **Last**: Jump to the final page
- **Percentage Display**: Shows current position (e.g., "Page 5000000 (50.00%)")

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── run.py                # Easy startup script
├── test_app.py           # Test suite
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── models/              # Data models
│   ├── all_key.py      # AllKey data class
│   └── blockchain.py   # Blockchain data class
├── services/            # Business logic services
│   ├── all_key_service.py    # Bitcoin key generation
│   └── balance_service.py    # Balance fetching
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── home.html        # Home page
    ├── search.html      # Search page
    ├── balance_scan.html # Balance scanner page
    └── about.html       # About page
```

## ⚙️ Configuration

The application uses a centralized configuration system (`config.py`):

### Core Settings
- **Addresses per Page**: 500 addresses displayed per page (configurable)
- **Search Limit**: 1000 pages (500,000 addresses) for address lookup
- **Balance Scan Limit**: 50 pages (25,000 addresses) per scan (Vercel optimized)
- **Total Pages**: 2.32×10⁷⁴ (scientific notation display)
- **Balance Checking**: Enable/disable real-time balance checking

### API Optimization
- **API Threads**: 10 concurrent threads for API requests
- **API Request Delay**: 0.05 seconds between API requests
- **API Chunk Size**: 200 addresses per API request
- **API Endpoint**: blockchain.info balance API
- **Caching**: In-memory caching for faster repeated requests
- **Batch Processing**: Single API call for multiple pages (10x faster)

### Performance Options

**For Maximum Speed** (disable balance checking):
```python
ENABLE_BALANCE_CHECKING = False  # In config.py
```
This makes page loads nearly instantaneous, similar to the original TypeScript version.

**For Balanced Performance** (with real-time data):
```python
ENABLE_BALANCE_CHECKING = True   # In config.py
```

You can easily modify these settings by editing the `config.py` file.

## 🔍 Find Address Functionality

The application includes a powerful search feature that allows you to find specific Bitcoin addresses:

### How to Use Find Address:
1. Navigate to the **Find Address** page from the main navigation
2. Enter a Bitcoin address in the search box
3. The system will find which page contains that address
4. You'll see the page number, position, private key, and address type
5. Click "Go to Page" to view the address in the main table
6. Use copy buttons (📋) to copy full addresses or private keys

### Example Searches:
- `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` (Page 1, Position 1, Compressed)
- `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm` (Page 1, Position 1, Uncompressed)

### Search Capabilities:
- **Search Limit**: 1000 pages (500,000 addresses) for performance
- **Address Types**: Works for both compressed and uncompressed addresses
- **Configurable**: Modify `MAX_SEARCH_PAGES` in `config.py` to change the limit
- **Fast Results**: Optimized search algorithm for quick address lookup

## 💰 Find Balances Functionality

The Find Balances feature is a powerful tool that allows you to scan multiple pages for addresses with actual Bitcoin balances:

### How to Use Find Balances:
1. Navigate to the **Find Balances** page from the main navigation
2. Set the **Starting Page** (any page number 1 or greater)
3. Set the **Pages to Scan** (1-50 pages per scan for optimal performance)
4. Click **"Start Scan"** to begin the process
5. View results showing only addresses with non-zero balances
6. Click page numbers to jump to that page in the main view
7. Use copy buttons (📋) to copy private keys or addresses

### Find Balances Features:
- **High-Speed Scanning**: Batch processing for 10x faster performance
- **Large Scale**: Scan up to 50 pages (25,000 addresses) per request (Vercel optimized)
- **Real-time Results**: Live balance data from blockchain APIs
- **Filtered Results**: Only shows addresses with actual Bitcoin balances
- **Easy Navigation**: Direct links to view addresses in the main table
- **Copy Functionality**: One-click copying of private keys and addresses

### Performance Examples:
- **10 pages**: ~5,000 addresses scanned in seconds
- **25 pages**: ~12,500 addresses scanned in under a minute
- **50 pages**: ~25,000 addresses scanned in 1-2 minutes (Vercel optimized)

### Technical Details:
- **Batch Processing**: Single API call for all addresses (much faster than page-by-page)
- **Optimized API**: Reduced delays and increased concurrency
- **Smart Filtering**: Only displays addresses with non-zero balances
- **Memory Efficient**: Processes large datasets without memory issues

## 📚 Dependencies

- **Flask**: Web framework for the application
- **requests**: HTTP client for API calls to blockchain.info
- **ecdsa**: Elliptic curve cryptography for key generation
- **base58**: Base58 encoding/decoding for Bitcoin addresses
- **cryptography**: Additional cryptographic functions

## 🔧 Technical Details

### Generation Algorithm
- **Private Key Format**: Uncompressed WIF (Wallet Import Format) private keys
- **Key Generation**: Sequential private keys starting from 1 (0x000...001 in hex)
- **Cryptographic Method**: ECDSA SECP256k1 curve
- **Address Format**: P2PKH (Pay-to-Public-Key-Hash) with Base58 encoding
- **Address Types**: Both compressed (33 bytes) and uncompressed (65 bytes) versions

### Display Features
- **Balance Display**: 5 decimal places with green highlighting for non-zero balances
- **Scientific Notation Pagination**: Professional display of page numbers (2.32×10⁷⁴ format)
- **Page Percentage Display**: Shows current position with 2 decimal precision
- **Truncated Display**: Private keys and addresses show first 7 and last 9 characters
- **Copy Functionality**: One-click copy buttons for full private keys and addresses
- **Page Totals**: Real-time total balance and received amounts in navigation bar
- **Enhanced Navigation**: First, Previous, Random, Next, Last buttons
- **Responsive Design**: Modern, mobile-friendly interface with Tailwind CSS

### Performance Features
- **API Integration**: Real-time balance checking via blockchain.info
- **Concurrent Processing**: 10 threads for parallel API requests
- **Batch Processing**: Single API call for multiple pages (10x faster)
- **Intelligent Caching**: In-memory cache for instant repeated requests
- **Configurable Settings**: Balance checking can be disabled for maximum speed
- **Optimized Chunking**: 200 addresses per API request for efficiency

## 🔬 Scientific Notation Feature

The application now displays page numbers in scientific notation to accurately represent the enormous scale of Bitcoin's private key space:

### Key Features:
- **Dynamic Calculation**: Based on actual Bitcoin max number (2²⁵⁶)
- **Professional Format**: Uses proper Unicode superscript characters (2.32×10⁷⁴)
- **Accurate Representation**: Shows the true scale of Bitcoin's private key space
- **Clean Display**: Much more readable than displaying the full number

### Technical Details:
- **Total Pages**: 2.32×10⁷⁴ (232 followed by 72 zeros!)
- **Format**: Coefficient × 10^exponent with Unicode superscripts
- **Implementation**: Dynamic calculation using `format_scientific_notation()` function
- **Display**: Both top and bottom navigation show scientific notation

### Example:
```
Instead of: 231584178474632390847141970017375815705675128558149808765210326283B
Shows:      2.32×10⁷⁴
```

This makes the pagination much more professional and mathematically accurate while being easily readable.

## 🧭 Enhanced Navigation Features

The application now includes comprehensive navigation controls for easy exploration of the massive Bitcoin key space:

### Navigation Buttons
- **First (⏮)**: Jump directly to page 1
- **Previous (←)**: Navigate to the previous page
- **Random (🎲)**: Jump to a random page for exploration
- **Next (→)**: Navigate to the next page
- **Last (⏭)**: Jump directly to the final page

### Page Position Display
- **Percentage Display**: Shows current position with 2 decimal precision
- **Example**: "Page 5000000 (50.00%)" indicates you're halfway through the key space
- **Real-time Updates**: Percentage updates automatically as you navigate
- **Scientific Notation**: Total pages displayed as 2.32×10⁷⁴

### User Experience Benefits
- **Quick Navigation**: Jump to any position in the key space instantly
- **Exploration**: Random page feature for discovering interesting addresses
- **Position Awareness**: Always know where you are in the massive dataset
- **Consistent Layout**: Navigation available at both top and bottom of pages

### Technical Implementation
- **Random Generation**: Uses Python's `random.randint()` for true randomness
- **Percentage Calculation**: `(current_page / max_page) * 100` with 2 decimal precision
- **Smart Disabling**: Buttons are disabled when at boundaries (page 1 or last page)
- **Responsive Design**: Navigation adapts to different screen sizes

## ⚠️ Security Notice

**This application is for educational purposes only.** The generated private keys are sequential and predictable, making them unsuitable for actual Bitcoin transactions. Never use these keys for real cryptocurrency operations.

## 📄 License

This project is based on the original Angular TypeScript implementation by [mingfunwong](https://github.com/mingfunwong/all-bitcoin-private-key).

## 🚀 Performance Comparison

| Feature | Original TypeScript | Python Version |
|---------|-------------------|----------------|
| Page Load Speed | Fast | Fast (with optimizations) |
| Balance Checking | Real-time | Real-time + Caching |
| Search Functionality | Limited | Enhanced (1000 pages) |
| Balance Scanner | Not Available | **NEW**: Multi-page scanning |
| Scientific Notation | Not Available | **NEW**: Professional pagination display |
| Enhanced Navigation | Basic (Previous/Next) | **NEW**: First, Previous, Random, Next, Last |
| Page Percentage | Not Available | **NEW**: 2 decimal precision position display |
| Page Totals | Not Available | **NEW**: Total balance and received amounts |
| Menu Names | Technical | **NEW**: Intuitive (Browse Keys, Find Address, etc.) |
| Copy Functionality | Basic | Advanced (truncated + copy) |
| Configuration | Fixed | Configurable |
| Performance | Good | Optimized (concurrent + batch processing) |

The Python version maintains all the functionality of the original while adding significant performance improvements, enhanced user experience features, and intuitive navigation controls.