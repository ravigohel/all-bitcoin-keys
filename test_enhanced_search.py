#!/usr/bin/env python3
"""
Test script for enhanced search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import find_address_page

def test_enhanced_search():
    """Test the enhanced search functionality with starting page parameter"""
    print("Testing Enhanced Search Functionality")
    print("=" * 50)
    
    # Test 1: Search from page 1 (default behavior)
    print("\n1. Testing search from page 1 (default):")
    result1 = find_address_page("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", 1)
    if result1:
        print(f"   ✓ Found address on page {result1['page']}, position {result1['position']}")
        print(f"   ✓ Type: {'Compressed' if result1['is_compressed'] else 'Uncompressed'}")
    else:
        print("   ✗ Address not found")
    
    # Test 2: Search from page 2 (should not find the same address)
    print("\n2. Testing search from page 2 (should not find page 1 address):")
    result2 = find_address_page("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", 2)
    if result2:
        print(f"   ✗ Unexpectedly found address on page {result2['page']}")
    else:
        print("   ✓ Correctly did not find address (as expected)")
    
    # Test 3: Search for uncompressed address from page 1
    print("\n3. Testing search for uncompressed address from page 1:")
    result3 = find_address_page("1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm", 1)
    if result3:
        print(f"   ✓ Found address on page {result3['page']}, position {result3['position']}")
        print(f"   ✓ Type: {'Compressed' if result3['is_compressed'] else 'Uncompressed'}")
    else:
        print("   ✗ Address not found")
    
    # Test 4: Search with invalid starting page
    print("\n4. Testing search with starting page beyond limit:")
    result4 = find_address_page("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", 1001)
    if result4:
        print(f"   ✗ Unexpectedly found address on page {result4['page']}")
    else:
        print("   ✓ Correctly did not find address (starting page too high)")
    
    print("\n" + "=" * 50)
    print("Enhanced search functionality test completed!")

if __name__ == "__main__":
    test_enhanced_search()
