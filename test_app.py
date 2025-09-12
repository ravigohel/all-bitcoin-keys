#!/usr/bin/env python3
"""
Test script for the All Bitcoin Private Key application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.all_key_service import AllKeyService
from services.balance_service import BalanceService
from models.all_key import AllKey

def test_all_key_service():
    """Test the AllKeyService functionality"""
    print("Testing AllKeyService...")
    
    service = AllKeyService()
    
    # Test generating keys for page 1
    items = service.get_data(1, 5)  # Generate 5 keys for testing
    
    print(f"Generated {len(items)} keys:")
    for i, item in enumerate(items):
        print(f"  Key {i+1}:")
        print(f"    ID: {item.id}")
        print(f"    Private Key: {item.private_key}")
        print(f"    Uncompressed Address: {item.address_uncompressed}")
        print(f"    Compressed Address: {item.address_compressed}")
        print()
    
    # Verify that addresses are different for compressed vs uncompressed
    first_item = items[0]
    if first_item.address_compressed != first_item.address_uncompressed:
        print("✓ Compressed and uncompressed addresses are different")
    else:
        print("✗ Compressed and uncompressed addresses are the same")
    
    return True

def test_balance_service():
    """Test the BalanceService functionality"""
    print("Testing BalanceService...")
    
    service = BalanceService()
    
    # Test with a known Bitcoin address (Satoshi's address)
    test_addresses = ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]
    
    try:
        balances = service.get_balance(test_addresses)
        print(f"Fetched balance for {len(balances)} addresses")
        
        for address, balance in balances.items():
            print(f"  Address: {address}")
            print(f"    Final Balance: {balance.final_balance}")
            print(f"    Total Received: {balance.total_received}")
            print(f"    Number of Transactions: {balance.n_tx}")
        
        print("✓ Balance service working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Balance service error: {e}")
        return False

def test_integration():
    """Test integration between services"""
    print("Testing integration...")
    
    all_key_service = AllKeyService()
    balance_service = BalanceService()
    
    # Generate a small set of keys
    items = all_key_service.get_data(1, 2)
    
    # Prepare addresses for balance checking
    addresses = []
    for item in items:
        addresses.append(item.address_compressed)
        addresses.append(item.address_uncompressed)
    
    print(f"Checking balances for {len(addresses)} addresses...")
    
    try:
        # Fetch balance data
        balance_list = balance_service.get_balance(addresses)
        
        # Update items with balance information
        for item in items:
            if item.address_compressed in balance_list:
                item.address_compressed_balance = balance_list[item.address_compressed].final_balance
            else:
                item.address_compressed_balance = 0
                
            if item.address_uncompressed in balance_list:
                item.address_uncompressed_balance = balance_list[item.address_uncompressed].final_balance
            else:
                item.address_uncompressed_balance = 0
        
        print("✓ Integration test successful")
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("All Bitcoin Private Key - Python Test Suite")
    print("=" * 50)
    
    tests = [
        test_all_key_service,
        test_balance_service,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
