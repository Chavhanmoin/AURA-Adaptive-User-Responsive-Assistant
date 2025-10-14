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
    # Use raw string (r'') or escape backslashes
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

else:
    print('Unsupported OS')
    exit(1)

# Register Chrome browser if available
try:
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
except Exception as e:
    print("Failed to register Chrome:", e)

def youtube(textToSearch: str) -> None:
    """
    Opens a new Chrome tab with YouTube search results for the given query.
    """
    if not textToSearch or textToSearch.strip().lower() == "none":
        print("Empty or invalid search query.")
        return

    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query

    try:
        webbrowser.get('chrome').open_new_tab(url)
    except webbrowser.Error:
        # Fallback to default browser if Chrome is not found
        print("Chrome not found, using default browser.")
        webbrowser.open_new_tab(url)

# For testing standalone
if __name__ == '__main__':
    youtube('any text')
