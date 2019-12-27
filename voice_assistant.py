### Step-1 Importing the libraries

import speech_recognition as sr
import os
import sys
import re
import webbrowser
import requests
from pyowm import OWM
import urllib
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipediaapi
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import geocoder
from webbrowser import open_new_tab
import pyjokes

### Step-2 Setting up voice input and output

#Getting voice input from the user
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('''\nMy name is Adam, I can do these things for you:\nCurrent weather in your city\nLatest News\nYour location\nTell you about things & people\nPlay a song on Youtube\nTell a joke\n'''
             )
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command
# Function to give voice output 
def response(audio):
    for line in audio.splitlines():
        os.system("say " + audio)

### Step-3 Adding functions to our Voice Assistant

def assistant(command):
    # current weather at your current location
    if 'weather' in command:
        f = open('/Users/ravidahiya/.secret/dark_api.json') #Loading my darksky api
        keys = json.load(f)
        api = keys['api_key']
        g = geocoder.ip('me') 
        latlong = g.latlng #Getting current lat-long
        weather = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(api,latlong[0],latlong[1]))
        weather = weather.json()
        print('Current weather: {}\nCurrent temperature: {}\nHumidity: {}\nVisibility: {}'.format(
            weather['currently']['summary'],weather['currently']['temperature'],weather['currently']['humidity'],
            weather['currently']['visibility']))
    
    #Getting top current news from google news feed
    elif 'news' in command:
        news_url="https://news.google.com/news/rss"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()
        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        for news in news_list[0:5]:
            try:
                print(news.title.text)
                print(news.link.text)
                print(news.pubDate.text)
                response(news.title.text) #Read the news
                print("-"*60)
            except Exception as e:
                print(e)
                
    #Getting desired topics from wikipedia            
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command) #to get the item to search in wikipedia
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(reg_ex.group(1))
        print(page.summary)
    
    #Getting current location
    elif 'where am i' in command or 'location' in command:
        g = geocoder.ip('me')
        latlong = g.latlng
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.reverse(latlong)
        print(location.address)
    
    #Playing video on youtube
    elif 'play' in command:
        reg_ex = re.search('play (.*)', command)
        URL = ("https://www.google.com/search?btnI=I'm+Feeling+Lucky&ie=UTF-8"
       "&oe=UTF-8&q=site:youtube.com%20inurl:http://www.youtube.com/"
       "watch?v=%20{0}".format(reg_ex.group(1)))
        open_new_tab(URL)
    
    #Getting a random joke from pyjokes library
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        response(joke)
    
    #exit
    elif 'exit' in command or 'quit' in command:
        sys.exit(1)
    
    #to get next commnand from the user
    while True:
        assistant(myCommand())
        
assistant(myCommand())