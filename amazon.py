import requests
from bs4 import BeautifulSoup
import webbrowser
from helpers import speak

def search_amazon_product(product_name):
    """Search for a product on Amazon"""
    try:
        product = product_name.replace('amazon', '').replace('search', '').strip()
        
        if not product:
            speak("What product should I search on Amazon?")
            return "No product specified"
        
        search_url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
        webbrowser.open(search_url)
        
        speak(f"Searching Amazon for {product}")
        return f"Amazon search opened for: {product}"
        
    except Exception as e:
        speak("Amazon search failed")
        return f"Error: {str(e)}"

def open_amazon():
    """Open Amazon homepage"""
    try:
        webbrowser.open("https://www.amazon.com")
        speak("Opening Amazon")
        return "Amazon opened successfully"
    except Exception as e:
        speak("Failed to open Amazon")
        return f"Error: {str(e)}"
