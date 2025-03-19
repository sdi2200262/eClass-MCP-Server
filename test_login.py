#!/usr/bin/env python3
"""
Test script for eClass login functionality with UoA's SSO.

This script tests the eClass client's ability to authenticate
with the UoA SSO service and access eClass using credentials from the .env file.
"""

import os
import time
from dotenv import load_dotenv
from eclass_client import EClassClient

def test_login():
    """Test the login functionality of the eClass client with UoA's SSO."""
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment
    url = os.getenv('ECLASS_URL')
    username = os.getenv('ECLASS_USERNAME')
    password = os.getenv('ECLASS_PASSWORD')
    
    # Check if credentials are provided
    if not all([url, username, password]):
        print("ERROR: Missing credentials in .env file")
        print("Please ensure ECLASS_URL, ECLASS_USERNAME, and ECLASS_PASSWORD are set")
        return False
    
    # Test with dummy credentials if username contains 'your_username'
    if 'your_username' in username:
        print("WARNING: You are using the default placeholder username.")
        print("Please update the .env file with your actual UoA credentials.")
        return False
    
    # Create client
    client = EClassClient(url)
    
    print(f"Testing login to {url} with username: {username}")
    print("Accessing login form...")
    print("Following SSO authentication flow...")
    print("This might take a moment...")
    
    start_time = time.time()
    
    # Attempt login
    success = client.login(username, password)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        print(f"\n✅ Login SUCCESSFUL! Authentication took {duration:.2f} seconds.")
        print("\nVerifying access by retrieving courses...")
        
        # Try to get courses to verify access
        courses = client.get_courses()
        
        if courses:
            print(f"Found {len(courses)} courses:")
            for i, course in enumerate(courses, 1):
                print(f"  {i}. {course['name']}")
        else:
            print("No courses found or unable to retrieve course list.")
        
        # Logout
        print("\nLogging out...")
        client.logout()
        return True
    else:
        print(f"\n❌ Login FAILED after {duration:.2f} seconds!")
        print("Please check your credentials and try again.")
        print("Make sure the eClass server is accessible and your account is active.")
        print("\nPossible issues:")
        print("1. Incorrect username or password")
        print("2. UoA's SSO service is temporarily unavailable")
        print("3. Your account might be locked due to too many failed attempts")
        print("4. Network connectivity issues")
        return False

if __name__ == "__main__":
    print("=== UoA eClass Login Test ===\n")
    print("This test will attempt to authenticate with UoA's SSO service")
    print("and access your eClass account\n")
    
    try:
        result = test_login()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        result = False
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        result = False
    
    print("\n=== Test Complete ===")
    print(f"Result: {'SUCCESS' if result else 'FAILURE'}") 