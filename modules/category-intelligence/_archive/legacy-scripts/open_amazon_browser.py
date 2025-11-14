#!/usr/bin/env python3
"""
Open browser for Amazon authentication.
This script opens a browser window so the user can authenticate with Amazon
before scraping product data.
"""

import webbrowser
import time

def open_amazon_for_auth():
    """Open Amazon in browser for user authentication."""

    print("="*70)
    print("AMAZON AUTHENTICATION REQUIRED")
    print("="*70)
    print()
    print("Opening Amazon in your browser...")
    print()
    print("INSTRUCTIONS:")
    print("1. Log in to your Amazon account")
    print("2. Complete any security challenges (captcha, 2FA, etc.)")
    print("3. Once logged in, keep the browser open")
    print("4. Return here and press ENTER when ready")
    print()
    print("="*70)

    # Open Amazon
    webbrowser.open('https://www.amazon.com/')

    # Wait for user confirmation
    input("\nPress ENTER when you're logged into Amazon and ready to continue...")

    print("\n✓ Ready to proceed with Amazon scraping")
    print("  You can now run Amazon scraping scripts")
    print()

if __name__ == "__main__":
    open_amazon_for_auth()
