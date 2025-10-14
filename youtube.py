import urllib.parse
import webbrowser
from sys import platform
import os

# Register Chrome browser path based on OS
if platform == "linux" or platform == "linux2":
    chrome_path = '/usr/bin/google-chrome'

elif platform == "darwin":
    chrome_path = 'open -a /Applications/Google\\ Chrome.app'

elif platform == "win32":
    # Try both possible Chrome locations
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    ]
    chrome_path = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    if not chrome_path:
        chrome_path = chrome_paths[0]  # Default fallback

else:
    print('Unsupported OS')
    exit(1)

# Register Chrome browser if available
if platform == "win32" and chrome_path:
    try:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        print(f"Chrome registered: {chrome_path}")
    except Exception as e:
        print(f"Failed to register Chrome: {e}")
else:
    try:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    except Exception as e:
        print(f"Failed to register Chrome: {e}")

def youtube(textToSearch: str) -> None:
    """
    Opens a new Chrome tab with YouTube search results for the given query.
    """
    if not textToSearch or textToSearch.strip().lower() == "none":
        print("Empty or invalid search query.")
        return

    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    print(f"Opening YouTube search: {url}")

    try:
        webbrowser.get('chrome').open_new_tab(url)
        print(f"✓ YouTube search opened for: {textToSearch}")
    except:
        # Fallback to default browser
        print("Using default browser for YouTube search")
        webbrowser.open_new_tab(url)
        print(f"✓ YouTube search opened for: {textToSearch}")

# For testing standalone
if __name__ == '__main__':
    youtube('any text')
