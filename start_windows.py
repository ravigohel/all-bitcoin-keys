#!/usr/bin/env python3
"""
Windows-optimized startup script for the All Bitcoin Private Key application
This script uses Flask CLI which is more stable on Windows
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import requests
        import ecdsa
        import base58
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    """Main startup function using Flask CLI"""
    print("=" * 60)
    print("All Bitcoin Private Key - Windows Optimized Startup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nStarting the application using Flask CLI...")
    print("The application will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        # Set Flask environment variables
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        
        # Use Flask CLI which is more stable on Windows
        result = subprocess.run([
            sys.executable, '-m', 'flask', 'run', 
            '--host=0.0.0.0', 
            '--port=5001',
            '--debug'
        ], capture_output=False, text=True)
        
        if result.returncode != 0:
            print(f"\nApplication exited with code: {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
    except Exception as e:
        print(f"\nError starting application: {e}")
        print("\n🔧 Alternative solutions:")
        print("1. Try running: python app.py")
        print("2. Try running: python run.py")
        print("3. Change the port in config.py")
        print("4. Restart your terminal")
        sys.exit(1)

if __name__ == "__main__":
    main()
