from flask import Flask, render_template, request, redirect, url_for
import requests
import time
from services.all_key_service import AllKeyService
from services.balance_service import BalanceService
from models.all_key import AllKey
from models.blockchain import Blockchain
from config import ADDRESSES_PER_PAGE, BITCOIN_MAX_NUMBER, FLASK_HOST, FLASK_PORT, FLASK_DEBUG, ENABLE_BALANCE_CHECKING, MAX_SEARCH_PAGES

app = Flask(__name__)

# Initialize services
all_key_service = AllKeyService()
balance_service = BalanceService()

@app.route('/')
def home():
    return redirect(url_for('home_page', page=1))

@app.route('/home')
def home_page():
    page = int(request.args.get('page', 1))
    limit_per_page = ADDRESSES_PER_PAGE
    
    # Get Bitcoin keys and addresses
    items = all_key_service.get_data(page, limit_per_page)
    
    # Update items with balance information (if enabled)
    if ENABLE_BALANCE_CHECKING:
        # Prepare addresses for balance checking
        addresses = []
        for item in items:
            addresses.append(item.address_compressed)
            addresses.append(item.address_uncompressed)
        
        # Fetch balance data
        balance_list = balance_service.get_balance(addresses)
        
        # Update items with balance information
        for item in items:
            item.address_compressed_balance = get_balance(
                item.address_compressed, balance_list, 'final_balance'
            )
            item.address_compressed_received = get_balance(
                item.address_compressed, balance_list, 'total_received'
            )
            item.address_uncompressed_balance = get_balance(
                item.address_uncompressed, balance_list, 'final_balance'
            )
            item.address_uncompressed_received = get_balance(
                item.address_uncompressed, balance_list, 'total_received'
            )
    else:
        # Set all balances to None for fast loading
        for item in items:
            item.address_compressed_balance = None
            item.address_compressed_received = None
            item.address_uncompressed_balance = None
            item.address_uncompressed_received = None
    
    # Calculate pagination - use the actual Bitcoin max number for scientific notation
    # This will show the true scale in scientific notation
    max_page = BITCOIN_MAX_NUMBER // limit_per_page
    
    # Calculate total balance and received for this page
    page_total_balance = calculate_page_total_balance(items)
    page_total_received = calculate_page_total_received(items)
    page_percentage = calculate_page_percentage(page, max_page)
    
    return render_template('home.html', 
                         items=items, 
                         page=page, 
                         max_page=max_page,
                         page_total_balance=page_total_balance,
                         page_total_received=page_total_received,
                         page_percentage=page_percentage,
                         table_header_columns=[
                             'privateKey', 'address', 'balance', 'received',
                             'compressed', 'balance', 'received'
                         ])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random')
def random_page():
    """Redirect to a random page"""
    import random
    limit_per_page = ADDRESSES_PER_PAGE
    max_page = BITCOIN_MAX_NUMBER // limit_per_page
    random_page_num = random.randint(1, max_page)
    return redirect(url_for('home_page', page=random_page_num))

@app.route('/balance-scan')
def balance_scan():
    """Scan pages for addresses with balances"""
    start_page = request.args.get('start_page', '').strip()
    max_pages = request.args.get('max_pages', '').strip()
    
    # If no parameters provided, just show the form
    if not start_page or not max_pages:
        return render_template('balance_scan.html')
    
    # Validate inputs
    try:
        start_page = int(start_page)
        max_pages = int(max_pages)
        if start_page < 1:
            return render_template('balance_scan.html', 
                                 start_page=start_page,
                                 max_pages=max_pages,
                                 error="Starting page must be 1 or greater")
        if max_pages < 1 or max_pages > 50:
            return render_template('balance_scan.html', 
                                 start_page=start_page,
                                 max_pages=max_pages,
                                 error="Max pages must be between 1 and 50 (Vercel optimized)")
    except ValueError:
        return render_template('balance_scan.html', 
                             start_page=start_page,
                             max_pages=max_pages,
                             error="Invalid page numbers")
    
    # Perform balance scan only when user submits the form
    results = scan_pages_for_balances(start_page, max_pages)
    
    return render_template('balance_scan.html', 
                         start_page=start_page,
                         max_pages=max_pages,
                         results=results,
                         total_found=len(results))

@app.route('/search')
def search():
    """Search for a specific Bitcoin address and find which page it's on"""
    address = request.args.get('address', '').strip()
    start_page = request.args.get('start_page', '1').strip()
    
    if not address:
        return render_template('search.html', error="Please enter an address to search")
    
    # Validate Bitcoin address format (basic check)
    if not (address.startswith('1') or address.startswith('3') or address.startswith('bc1')):
        return render_template('search.html', error="Invalid Bitcoin address format")
    
    # Validate and parse starting page
    try:
        start_page = int(start_page)
        if start_page < 1:
            return render_template('search.html', 
                                 address=address, 
                                 start_page=start_page,
                                 error="Starting page must be 1 or greater")
    except ValueError:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             error="Invalid starting page number")
    
    # Search for the address
    result = find_address_page(address, start_page)
    
    if result:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             page=result['page'], 
                             position=result['position'],
                             private_key=result['private_key'],
                             is_compressed=result['is_compressed'])
    else:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             error=f"Address not found in pages {start_page} to {start_page + MAX_SEARCH_PAGES - 1}")

def find_address_page(target_address, start_page=1):
    """Find which page contains a specific Bitcoin address"""
    # We need to search through the generated addresses
    # This is computationally expensive, so we'll use a smart search approach
    
    # Search through MAX_SEARCH_PAGES starting from the specified start_page
    end_page = start_page + MAX_SEARCH_PAGES - 1
    
    for page in range(start_page, end_page + 1):
        items = all_key_service.get_data(page, ADDRESSES_PER_PAGE)
        
        for i, item in enumerate(items):
            if item.address_compressed == target_address:
                return {
                    'page': page,
                    'position': i + 1,
                    'private_key': item.private_key,
                    'is_compressed': True
                }
            elif item.address_uncompressed == target_address:
                return {
                    'page': page,
                    'position': i + 1,
                    'private_key': item.private_key,
                    'is_compressed': False
                }
    
    # If not found in the search range, return None
    return None

def get_balance(address, balance_list, balance_type):
    """Get balance for a specific address and type"""
    if address in balance_list:
        blockchain_obj = balance_list[address]
        if balance_type == 'final_balance':
            return blockchain_obj.final_balance
        elif balance_type == 'total_received':
            return blockchain_obj.total_received
        elif balance_type == 'n_tx':
            return blockchain_obj.n_tx
    return 0

def get_balance_class(balance):
    """Get CSS class based on balance value"""
    return 'text-green-700 font-semibold' if balance else 'text-slate-400'

def format_balance(balance):
    """Format balance for display"""
    if balance is not None:
        return f"{balance / (10**8):.5f} BTC"
    return "..."

def truncate_text(text, start_chars=4, end_chars=3):
    """Truncate text to show only start and end characters with dots in between"""
    if not text or len(text) <= start_chars + end_chars:
        return text
    return f"{text[:start_chars]}...{text[-end_chars:]}"

def format_page_number(page_num):
    """Format large page numbers to be more readable"""
    try:
        # Convert to int if it's a string
        if isinstance(page_num, str):
            page_num = int(page_num)
        
        if page_num < 1000:
            return str(page_num)
        elif page_num < 1000000:
            return f"{page_num // 1000}K"
        elif page_num < 1000000000:
            return f"{page_num // 1000000}M"
        else:
            return f"{page_num // 1000000000}B"
    except (ValueError, TypeError):
        # If conversion fails, return a simplified version
        return "∞"

def format_scientific_notation(number):
    """Format large numbers in scientific notation"""
    try:
        if isinstance(number, str):
            number = int(number)
        
        if number < 1000:
            return str(number)
        else:
            # Convert to scientific notation
            import math
            exponent = int(math.log10(number))
            coefficient = number / (10 ** exponent)
            
            # Round coefficient to 2 decimal places
            coefficient = round(coefficient, 2)
            
            # Use proper superscript characters
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
            }
            
            exponent_str = ''.join(superscript_map.get(digit, digit) for digit in str(exponent))
            return f"{coefficient}×10{exponent_str}"
    except (ValueError, TypeError, OverflowError):
        # For extremely large numbers, use a fallback
        return "2.8×10²³"

def calculate_page_total_balance(items):
    """Calculate total balance for all addresses on the current page"""
    total_balance = 0
    for item in items:
        if item.address_compressed_balance:
            total_balance += item.address_compressed_balance
        if item.address_uncompressed_balance:
            total_balance += item.address_uncompressed_balance
    return total_balance

def calculate_page_total_received(items):
    """Calculate total received balance for all addresses on the current page"""
    total_received = 0
    for item in items:
        if item.address_compressed_received:
            total_received += item.address_compressed_received
        if item.address_uncompressed_received:
            total_received += item.address_uncompressed_received
    return total_received

def calculate_page_percentage(current_page, max_page):
    """Calculate the percentage of current page position within total pages"""
    if max_page <= 0:
        return 0.00
    percentage = (current_page / max_page) * 100
    return round(percentage, 2)

def scan_pages_for_balances(start_page, max_pages):
    """Scan multiple pages for addresses with balances - Optimized for speed"""
    results = []
    end_page = start_page + max_pages - 1
    
    # Collect all addresses from all pages first
    all_items = []
    for page in range(start_page, end_page + 1):
        items = all_key_service.get_data(page, ADDRESSES_PER_PAGE)
        for item in items:
            item.page_number = page  # Store page number with item
            all_items.append(item)
    
    # Prepare all addresses for batch balance checking
    all_addresses = []
    for item in all_items:
        all_addresses.append(item.address_compressed)
        all_addresses.append(item.address_uncompressed)
    
    # Single batch API call for all addresses (much faster!)
    balance_list = balance_service.get_balance(all_addresses)
    
    # Process results
    for item in all_items:
        compressed_balance = get_balance(item.address_compressed, balance_list, 'final_balance')
        uncompressed_balance = get_balance(item.address_uncompressed, balance_list, 'final_balance')
        
        # If either address has a balance, add to results
        if compressed_balance > 0 or uncompressed_balance > 0:
            results.append({
                'page': item.page_number,
                'private_key': item.private_key,
                'address_compressed': item.address_compressed,
                'address_uncompressed': item.address_uncompressed,
                'compressed_balance': compressed_balance,
                'uncompressed_balance': uncompressed_balance,
                'compressed_received': get_balance(item.address_compressed, balance_list, 'total_received'),
                'uncompressed_received': get_balance(item.address_uncompressed, balance_list, 'total_received')
            })
    
    return results

# Make functions available in templates
app.jinja_env.globals.update(
    get_balance_class=get_balance_class,
    format_balance=format_balance,
    truncate_text=truncate_text,
    format_page_number=format_page_number,
    format_scientific_notation=format_scientific_notation,
    calculate_page_total_balance=calculate_page_total_balance,
    calculate_page_percentage=calculate_page_percentage,
    MAX_SEARCH_PAGES=MAX_SEARCH_PAGES,
    ADDRESSES_PER_PAGE=ADDRESSES_PER_PAGE
)

# For Vercel deployment
app = app

def cleanup_resources():
    """Clean up resources on shutdown"""
    try:
        # Clean up balance service
        if hasattr(balance_service, '_cleanup'):
            balance_service._cleanup()
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    import atexit
    import signal
    import sys
    
    # Register cleanup handlers
    atexit.register(cleanup_resources)
    
    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n🛑 Shutting down gracefully...")
        cleanup_resources()
        sys.exit(0)
    
    # Register signal handlers for graceful shutdown
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    if hasattr(signal, 'SIGINT'):
        signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Use threaded=True and use_reloader=False for better Windows compatibility
        app.run(
            debug=FLASK_DEBUG, 
            host=FLASK_HOST, 
            port=FLASK_PORT,
            threaded=True,
            use_reloader=False,  # Disable reloader to avoid socket issues on Windows
            use_debugger=FLASK_DEBUG
        )
    except OSError as e:
        if hasattr(e, 'winerror') and e.winerror == 10038:  # Windows socket error
            print("\n" + "="*60)
            print("⚠️  Windows Socket Error Detected")
            print("="*60)
            print("This is a known issue with Flask's development server on Windows.")
            print("\n🔧 Solutions:")
            print("1. Try running the application again")
            print("2. Use a different port (change FLASK_PORT in config.py)")
            print("3. Use the run.py script instead: python run.py")
            print("4. Use the Windows-optimized script: python start_windows.py")
            print("5. For production, use a proper WSGI server like Gunicorn")
            print("\n💡 Alternative startup command:")
            print(f"   python -m flask run --host={FLASK_HOST} --port={FLASK_PORT}")
            print("="*60)
        else:
            print(f"Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        cleanup_resources()
    except Exception as e:
        print(f"Unexpected error: {e}")
        cleanup_resources()
