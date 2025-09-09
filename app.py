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
    
    # Calculate pagination
    max_page = BITCOIN_MAX_NUMBER // limit_per_page
    
    # Calculate total balance for this page
    page_total_balance = calculate_page_total_balance(items)
    
    return render_template('home.html', 
                         items=items, 
                         page=page, 
                         max_page=max_page,
                         page_total_balance=page_total_balance,
                         table_header_columns=[
                             'privateKey', 'address', 'balance', 'received',
                             'compressed', 'balance', 'received'
                         ])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    """Search for a specific Bitcoin address and find which page it's on"""
    address = request.args.get('address', '').strip()
    
    if not address:
        return render_template('search.html', error="Please enter an address to search")
    
    # Validate Bitcoin address format (basic check)
    if not (address.startswith('1') or address.startswith('3') or address.startswith('bc1')):
        return render_template('search.html', error="Invalid Bitcoin address format")
    
    # Search for the address
    result = find_address_page(address)
    
    if result:
        return render_template('search.html', 
                             address=address, 
                             page=result['page'], 
                             position=result['position'],
                             private_key=result['private_key'],
                             is_compressed=result['is_compressed'])
    else:
        return render_template('search.html', 
                             address=address, 
                             error="Address not found in the generated sequence")

def find_address_page(target_address):
    """Find which page contains a specific Bitcoin address"""
    # We need to search through the generated addresses
    # This is computationally expensive, so we'll use a smart search approach
    
    # First, let's try a few pages to see if we can find it quickly
    for page in range(1, MAX_SEARCH_PAGES + 1):
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
    
    # If not found in first 100 pages, return None
    # Note: For addresses beyond page 100, you would need a more sophisticated search algorithm
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

def calculate_page_total_balance(items):
    """Calculate total balance for all addresses on the current page"""
    total_balance = 0
    for item in items:
        if item.address_compressed_balance:
            total_balance += item.address_compressed_balance
        if item.address_uncompressed_balance:
            total_balance += item.address_uncompressed_balance
    return total_balance

# Make functions available in templates
app.jinja_env.globals.update(
    get_balance_class=get_balance_class,
    format_balance=format_balance,
    truncate_text=truncate_text,
    calculate_page_total_balance=calculate_page_total_balance
)

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
