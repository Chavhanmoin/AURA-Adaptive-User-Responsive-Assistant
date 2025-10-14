#!/usr/bin/env python3
"""Test YouTube automation functionality"""

import time
from youtube import youtube

def test_youtube_search():
    """Test basic YouTube search functionality"""
    print("Testing YouTube search...")
    
    test_queries = [
        "python tutorial",
        "AI assistant",
        "machine learning basics"
    ]
    
    for query in test_queries:
        print(f"Searching for: {query}")
        youtube(query)
        time.sleep(2)  # Wait between searches
        print(f"✓ Search completed for: {query}")
    
    print("All YouTube tests completed!")

if __name__ == "__main__":
    test_youtube_search()