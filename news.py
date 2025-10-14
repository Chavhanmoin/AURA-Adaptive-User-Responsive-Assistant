import requests
import json
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def speak_news():
    try:
        url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=63cb4d5c87b14302b43c588535b47bc9'
        news = requests.get(url).text
        news_dict = json.loads(news)
        
        if 'articles' in news_dict:
            arts = news_dict['articles']
            speak('Source: The Times Of India')
            speak('Todays Headlines are..')
            for index, articles in enumerate(arts):
                speak(articles['title'])
                if index == len(arts)-1:
                    break
                speak('Moving on the next news headline..')
            speak('These were the top headlines, Have a nice day Sir!!..')
        else:
            speak('Sorry, unable to fetch news at the moment')
    except Exception as e:
        speak('Sorry, there was an error getting the news')

def getNewsUrl():
    return 'https://timesofindia.indiatimes.com/'

if __name__ == '__main__':
    speak_news()
