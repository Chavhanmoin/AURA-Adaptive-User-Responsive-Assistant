import wikipedia
import webbrowser
from helpers import speak

def search_and_open_wikipedia(query):
    """Search Wikipedia and open the article in browser"""
    try:
        # Remove 'wikipedia' from query if present
        search_term = query.replace('wikipedia', '').strip()
        
        if not search_term:
            speak("What should I search on Wikipedia?")
            return "No search term provided"
        
        speak(f"Searching Wikipedia for {search_term}")
        
        # Search for the page
        page = wikipedia.page(search_term)
        
        # Open the Wikipedia page in browser
        webbrowser.open(page.url)
        
        # Speak summary
        summary = wikipedia.summary(search_term, sentences=2)
        speak(f"Opening Wikipedia article for {search_term}")
        speak(summary)
        
        return f"Wikipedia article opened for: {search_term}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle multiple matches - use first option
        try:
            page = wikipedia.page(e.options[0])
            webbrowser.open(page.url)
            speak(f"Opening Wikipedia article for {e.options[0]}")
            return f"Wikipedia article opened for: {e.options[0]}"
        except:
            speak("Multiple articles found. Please be more specific.")
            return "Disambiguation error"
            
    except wikipedia.exceptions.PageError:
        speak(f"No Wikipedia article found for {search_term}")
        return f"No article found for: {search_term}"
        
    except Exception as e:
        speak("Wikipedia search failed")
        return f"Error: {str(e)}"

def wikipedia_voice_search():
    """Interactive Wikipedia search"""
    from helpers import takeCommand
    
    speak("What do you want to search on Wikipedia?")
    query = takeCommand()
    
    if query and query != 'none':
        return search_and_open_wikipedia(query)
    else:
        speak("No search term received")
        return "No input received"