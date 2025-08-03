#!/usr/bin/env python3
"""
Test script for ALX Travel App API
This script demonstrates how to use the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_listings_endpoints():
    """Test listings endpoints"""
    print("=== Testing Listings Endpoints ===")
    
    # Get all listings
    print("\n1. Getting all listings...")
    response = requests.get(f"{BASE_URL}/listings/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} listings")
        if data['results']:
            print(f"   First listing: {data['results'][0]['title']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Get available listings
    print("\n2. Getting available listings...")
    response = requests.get(f"{BASE_URL}/listings/available/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {len(data)} available listings")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Get a specific listing
    print("\n3. Getting specific listing...")
    response = requests.get(f"{BASE_URL}/listings/1/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Listing: {data['title']}")
        print(f"   Price: ${data['price_per_night']}/night")
        print(f"   Rating: {data['average_rating']}/5 ({data['review_count']} reviews)")
    else:
        print(f"✗ Error: {response.status_code}")

def test_reviews_endpoints():
    """Test reviews endpoints"""
    print("\n=== Testing Reviews Endpoints ===")
    
    # Get all reviews
    print("\n1. Getting all reviews...")
    response = requests.get(f"{BASE_URL}/reviews/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} reviews")
        if data['results']:
            print(f"   First review: {data['results'][0]['rating']}/5 stars")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Get reviews for a specific listing
    print("\n2. Getting reviews for listing 1...")
    response = requests.get(f"{BASE_URL}/listings/1/reviews/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {len(data)} reviews for listing 1")
    else:
        print(f"✗ Error: {response.status_code}")

def test_bookings_endpoints():
    """Test bookings endpoints (authentication required)"""
    print("\n=== Testing Bookings Endpoints ===")
    
    # Try to get bookings without authentication
    print("\n1. Getting bookings (no auth)...")
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 401:
        print("✓ Correctly requires authentication")
    else:
        print(f"✗ Unexpected response: {response.status_code}")

def test_api_root():
    """Test API root endpoint"""
    print("=== Testing API Root ===")
    
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print("✓ API root accessible")
        print("Available endpoints:")
        for endpoint, url in data.items():
            print(f"  - {endpoint}: {url}")
    else:
        print(f"✗ Error accessing API root: {response.status_code}")

def main():
    """Main test function"""
    print("ALX Travel App API Test")
    print("=" * 50)
    
    try:
        test_api_root()
        test_listings_endpoints()
        test_reviews_endpoints()
        test_bookings_endpoints()
        
        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        print("\nTo test authenticated endpoints:")
        print("1. Create a user account")
        print("2. Use Basic Authentication or Session Authentication")
        print("3. Test POST, PUT, DELETE operations")
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the API server")
        print("Make sure the Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main() 