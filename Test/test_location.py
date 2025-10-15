#!/usr/bin/env python3
"""Test Location Detection"""

import geocoder
import requests

def test_geocoder():
    """Test geocoder location detection"""
    print("Testing geocoder...")
    
    try:
        g = geocoder.ip('me')
        print(f"City: {g.city}")
        print(f"Country: {g.country}")
        print(f"Lat/Lng: {g.latlng}")
        return g.city
    except Exception as e:
        print(f"Geocoder failed: {e}")
        return None

def test_ip_location():
    """Test IP-based location"""
    print("\nTesting IP location...")
    
    try:
        response = requests.get('http://ipinfo.io/json')
        data = response.json()
        city = data.get('city', 'Unknown')
        print(f"IP Location: {city}")
        return city
    except Exception as e:
        print(f"IP location failed: {e}")
        return None

if __name__ == "__main__":
    print("Location Detection Test")
    print("=" * 25)
    
    city1 = test_geocoder()
    city2 = test_ip_location()
    
    if city1 or city2:
        print(f"\nDetected location: {city1 or city2}")
    else:
        print("\nLocation detection failed")